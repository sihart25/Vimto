import datetime

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django_countries.fields import CountryField
from django.utils.translation import ugettext as _

from vimto_auth.models import UserDetails


class VimtoUserAuthenticationForm(AuthenticationForm):
    '''Overwriting the clean function to get lowercase username'''
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username.lower(),
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class PasswordCheckMixin(object):

    def check_password(self, passwd):
        ''' Basic checks for password strength. '''
        min_length = 6
        msg = ("Password should be at least " + str(min_length) + " characters long. "
               "It should contain a mixture of numbers and characters and contain both "
               "upper and lower case characters.")
        if passwd and len(passwd) < min_length:
            raise forms.ValidationError(_('Password too short: %(msg)s'), params={'msg': msg})

        if sum(c.isdigit() for c in passwd) < 1:
            raise forms.ValidationError(_('Password does not contain any numbers: %(msg)s'), params={'msg': msg})

        # check for upper/lower case letter
        if not any(c.isupper() for c in passwd) or not any(c.islower() for c in passwd):
            raise forms.ValidationError(_('Password does not contain both upper and lower case letter: %(msg)s'),
                                        params={'msg': msg})
        return passwd


class VimtoSetPasswordForm(SetPasswordForm, PasswordCheckMixin):

    def clean_new_password1(self):
        ''' Basic checks for password strength. '''
        return self.check_password(self.cleaned_data.get('new_password1'))


class VimtoUserCreationForm(UserCreationForm, PasswordCheckMixin):
    '''Extended user form with is_terms_agreed field'''
    is_terms_agreed = forms.BooleanField(label="Terms and conditions", required=True)
    email = forms.EmailField(label="Email address", max_length=254, required=True)
    username = forms.CharField(max_length=30, min_length=2, label="Username", required=True)
    first_name = forms.CharField(max_length=30, label="First name", required=True)
    last_name = forms.CharField(max_length=30, label="Last name", required=True)
    job_title = forms.ChoiceField(choices=UserDetails.JOB_TYPE, label="JobTitle", required=True)
    country = CountryField().formfield(initial='GB')
    is_active = False

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "job_title", "country",
                  "password1", "password2", "is_terms_agreed", "is_active")

    def clean_username(self):
        ''' Change username to lowercase. '''
        username = self.cleaned_data['username'].lower()
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(_('A user with that username already exists'))
        except User.DoesNotExist:
            return username

    def clean_password1(self):
        ''' Basic checks for password strength. '''
        return self.check_password(self.cleaned_data['password1'])

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserDetails without database save")

        user = super(VimtoUserCreationForm, self).save(commit=True)
        user_details = UserDetails(user=user,
                                   is_terms_agreed=self.cleaned_data['is_terms_agreed'],
                                   activation_key=default_token_generator.make_token(user),
                                   key_expires=(timezone.now() + datetime.timedelta(2)),
                                   job_title=self.cleaned_data['job_title'],
                                   country=self.cleaned_data['country'])
        user_details.save()
        return user_details
