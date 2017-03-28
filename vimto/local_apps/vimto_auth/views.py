from django.contrib.auth import views as auth_views

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout
from django.core.context_processors import csrf
from django.template.context import RequestContext
from vimto_auth.forms import VimtoUserAuthenticationForm
from vimto_auth.forms import VimtoUserCreationForm
from django.core.mail import send_mail
from django.utils import timezone
from vimto_auth.models import UserDetails
from django.conf import settings


def login_user(request, template_name='registration/login.html', extra_context=None):
    ''' Intercepts the login call and delegates to auth login. '''
    if 'remember_me' in request.POST:
        request.session.set_expiry(1209600)  # 2 weeks

    response = auth_views.login(request, template_name=template_name,
                                authentication_form=VimtoUserAuthenticationForm,
                                extra_context=extra_context)
    return response


def registration_complete(request):
    ''' Renders registration complete page. '''
    return render(request, 'registration/registration_form_complete.html')


def register(request, extra_context=None):
    ''' Register a new user after agreeing to terms and condition. '''

    token = {}
    if request.method == 'POST':
        form = VimtoUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            new_user = authenticate(username=form.cleaned_data['username'].lower(),
                                    password=form.cleaned_data['password1'],
                                    email=form.cleaned_data['email'],
                                    is_terms_agreed=form.cleaned_data['is_terms_agreed'])
            # login(request, new_user)
            if new_user and new_user.is_authenticated:
                '''We have to login once so the last login date is set'''
                login(request, new_user)

                request_context = RequestContext(request)
                request_context.push({"username": new_user.username})
                request_context.push({"first_name": new_user.first_name})
                request_context.push({"last_name": new_user.last_name})
                request_context.push({"email": new_user.email})

                logout(request)

                has_send = send_email_confirmation(request, new_user)
                if has_send:
                    request_context.push({"success_registration": True})
                    return render(request, 'registration/registration_form_complete.html', request_context)
                else:
                    request_context.push({"failure_registration": True})
                    return render(request, 'registration/registration_form_complete.html', request_context)
            else:
                print('new_user is not authenticated')
        else:
            '''not a valid form'''
            # print(form.error_messages)
    else:
        form = VimtoUserCreationForm()

    token.update(csrf(request))
    token['form'] = form
    return render(request, 'registration/registration_form.html', token)


def send_email_confirmation(request, new_user):
    ''' Sends an email with activation key to the user. '''
    token = new_user.userdetails.activation_key
    host = request.get_host()
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'

    # Send an email with the confirmation link
    email_subject = 'Vimto account confirmation'
    email_body = ("Dear %s, \n\nThank you for signing up for a Vimto account. \n\n"
                  "Your username is: %s \n\n"
                  "To activate your account, click the link within 48 hours:\n\n"
                  "%s://%s/accounts/user/activate/%s \n\n"
                  "Yours Sincerely,\n\nVimto Team") % (new_user.get_full_name(),
                                                          new_user.username,
                                                          protocol, host, token)
    has_send = send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [new_user.email])
    return has_send


def activate(request, activation_key):
    ''' View to activate the user by enabling is_activate, provided the right
    activation_key is given and the link was activated before the expiry period. '''

    request_context = RequestContext(request)
    request_context.push({"login_url": '/accounts/login/'})

    if request.user.is_authenticated():
        '''if user is authenticated, it means he is already a registered user'''
        request_context.push({"has_account": True})
        return render(request, 'registration/registration_form_complete.html', request_context)

    user_details = get_object_or_404(UserDetails,
                                     activation_key=activation_key)

    if user_details.key_expires < timezone.now():
        '''key has expired'''
        request_context.push({"expired": True})
        return render(request, 'registration/registration_form_complete.html', request_context)

    user_account = user_details.user
    user_account.is_active = True
    user_account.save()

    request_context.push({"success_activation": True})
    if not user_account.is_anonymous():
        request_context.push({"username": user_account.username})
        request_context.push({"first_name": user_account.first_name})
        request_context.push({"last_name": user_account.last_name})
    return render(request, 'registration/registration_form_complete.html', request_context)
