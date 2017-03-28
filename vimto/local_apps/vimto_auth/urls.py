'''URLs for pydgin_auth and  django auth'''
from django.conf.urls import url
from django.contrib import admin
import django.contrib.auth.views
import vimto_auth.views
from django.conf import settings
from vimto_auth.views import activate
from vimto_auth.forms import VimtoSetPasswordForm

admin.autodiscover()

try:
    base_html_dir = settings.BASE_HTML_DIR
except AttributeError:
    base_html_dir = ''

# Registration URLs
urlpatterns = [
    url(r'^login/$',  vimto_auth.views.login_user, name="login"),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/'}),
    url(r'^register/$', vimto_auth.views.register, name='registration'),
    url(r'^register/complete/$', vimto_auth.views.registration_complete),
    url(r'^user/activate/(?P<activation_key>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='user_activation_link'),
    #
    # password reset
    url(r'^user/password/reset/$', django.contrib.auth.views.password_reset,
        {
         'post_reset_redirect': '/accounts/user/password/reset/done/',
         'template_name': 'registration/admin/password_reset_form.html',
         'email_template_name': 'registration/admin/password_reset_email.html',
        },
        name="password_reset"),
    url(r'^user/password/reset/done/$', django.contrib.auth.views.password_reset_done,
        {'template_name': 'registration/admin/password_reset_done.html'}),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        django.contrib.auth.views.password_reset_confirm,
        {
         'post_reset_redirect': '/accounts/user/password/done/',
         'template_name': 'registration/admin/password_reset_confirm.html',
         'set_password_form': VimtoSetPasswordForm
         },
        name="password_reset_confirm"),
    url(r'^user/password/done/$', django.contrib.auth.views.password_reset_complete,
        {'template_name': 'registration/admin/password_reset_complete.html'}),
]
