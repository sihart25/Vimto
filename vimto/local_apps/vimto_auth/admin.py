
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from vimto_auth.models import UserDetails


# Define an inline admin descriptor for UserDetails model
# which acts a bit like a singleton
# http://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
class UserDetailsInline(admin.StackedInline):
    model = UserDetails
    can_delete = False
    verbose_name_plural = 'userdetails'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserDetailsInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
