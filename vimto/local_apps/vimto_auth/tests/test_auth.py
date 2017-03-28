import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient

from vimto_auth.forms import VimtoUserCreationForm,\
    VimtoUserAuthenticationForm, VimtoSetPasswordForm
from vimto_auth.models import UserDetails
import copy
from django.utils.encoding import force_text


class VimtouthTests(TestCase):
    TEST_DATA_DIR = os.path.join(settings.PROJECT_DIR, 'tests', 'data')

    def setUp(self):
        ''' Create a user and set up the test client. '''
        self.factory = APIRequestFactory()
        self.client = APIClient(enforce_csrf_checks=False)
        self.user = User.objects.create_user('testuser', email='testuser@test.com',
                                             password='testing')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_login(self):
        ''' Test login possible. '''
        self.assertTrue(
            self.client.login(username='testuser', password='testing'))

    def test_login_view(self):
        ''' Test login view POSTing. '''
        url = reverse('accounts:login')
        response = self.client.post(url, data={'username': 'testuser', 'password': 'testing', 'remember_me': True})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, '/')

    def test_token(self):
        ''' Test token authentication. '''
        (user, _token) = TokenAuthentication().authenticate_credentials(self.token.key)
        self.assertTrue(user.is_authenticated())

    def test_invalid_login_form(self):
        ''' Test the authentication form produces an error. '''
        auth_form = VimtoUserAuthenticationForm(data={'username': 'testuser',
                                                         'password': 'wrong_password'})
        self.assertFalse(auth_form.is_valid())
        self.assertTrue('Please enter a correct username and password' in auth_form.errors.as_text())

    def test_password_reset_form(self):
        ''' Test the reset password form. '''
        self.assertTrue(VimtoSetPasswordForm(user=User.objects.get(username='testuser'),
                                                data={'new_password1': 'Xyzxyz1',
                                                      'new_password2': 'Xyzxyz1'}).is_valid())


class RegistrationTests(TestCase):
    ''' New user registration tests. '''

    def setUp(self):
        ''' Create a user and set up the test client. '''
        self.form_data = {'first_name': 'John', 'last_name': 'Smith', 'username': 'test',
                          'country': 'GB', 'email': 'john@example.com',
                          'password1': 'Xyzxyz1', 'password2': 'Xyzxyz1',
                          'job_title': UserDetails.RESE, 'is_terms_agreed': True}
        self.url = reverse('accounts:registration')

    def test_new_user_form(self):
        ''' Test the user registration form is valid. '''
        self.assertTrue(VimtoUserCreationForm(data=self.form_data).is_valid())

    def test_new_user_form_save(self):
        ''' Test the user registration form test user creation and activation. '''
        user_details = VimtoUserCreationForm(data=self.form_data).save()
        users = User.objects.filter(username=user_details.user.username)
        self.assertTrue(users.exists())

        # test authentication with and without activation
        user = users.get(username=self.form_data['username'])
        auth_form = VimtoUserAuthenticationForm(data={'username': self.form_data['username'],
                                                         'password': self.form_data['password1']})
        self.assertTrue('This account is inactive' in auth_form.errors.as_text())
        self.assertFalse(auth_form.is_valid())

        # activate user
        user.is_active = True
        user.save(update_fields=["is_active"])

        auth_form = VimtoUserAuthenticationForm(data={'username': self.form_data['username'],
                                                         'password': self.form_data['password1']})
        self.assertTrue(auth_form.is_valid())

    def test_user_registration_form_password_error(self):
        ''' Test the user registration form with a password error. '''
        form_data = copy.copy(self.form_data)
        form_data['password1'] = 'xyz'
        form_data['password2'] = 'xyz'
        response = self.client.post(self.url, form_data)
        self.assertContains(response, "Password too short", status_code=status.HTTP_200_OK)

    def test_new_user_form_password_error2(self):
        ''' Test the user registration form with a password error. '''
        form_data = copy.copy(self.form_data)
        form_data['password1'] = 'xyz123'
        form_data['password2'] = 'xyz123'
        response = self.client.post(self.url, form_data)
        self.assertContains(response, "Password does not contain both upper and lower case letter",
                            status_code=status.HTTP_200_OK)

    def test_new_user_form_password_error3(self):
        ''' Test the user registration form with a password error. '''
        form_data = copy.copy(self.form_data)
        form_data['password1'] = 'xyzxyz'
        form_data['password2'] = 'xyzxyz'
        response = self.client.post(self.url, form_data)
        self.assertContains(response, "Password does not contain any numbers",
                            status_code=status.HTTP_200_OK)

    def test_new_user_form_view(self):
        ''' Test the user registration form with a password error. '''
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("Thank you for registering" in force_text(response.content))

    def test_new_user_activation_form(self):
        ''' Test the user activation form. '''
        form_data = copy.copy(self.form_data)
        form_data['username'] = 'my_username'
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("Thank you for registering" in force_text(response.content))
        user = User.objects.get(username=form_data['username'])
        user_details = UserDetails.objects.get(user=user)
        self.assertFalse(user.is_active)

        # now activate user
        activation_url = reverse('accounts:user_activation_link',
                                 kwargs={'activation_key': user_details.activation_key})
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
