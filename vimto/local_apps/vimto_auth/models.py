from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django_countries.fields import CountryField


class UserDetails(models.Model):
    """
    Model to hold additional details about a user, e.g. telephone, job title/description.
    """
    
    RESE = 'RESE'
    OTHER = 'OTHER'
    SOFT = 'SOFT'
    JOB_TYPE = (
        (RESE, 'Researcher'),
        (SOFT, 'Software Company'),
        (OTHER, 'Other Industry Professional'),
    )

    user = models.OneToOneField(User)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone no. in the format: '+999999999' up to 15 digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16, blank=True)
    job_title = models.CharField(max_length=25, choices=JOB_TYPE,)
    country = CountryField(blank_label='(select country)')

    is_terms_agreed = models.BooleanField(default=False)
    # account activation key and expiry
    activation_key = models.CharField(max_length=40, null=True, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)

    User._meta.get_field('email')._unique = True  # @UndefinedVariable
    # Create profile automatically when referenced
    # User.userdetails = property(lambda u: UserDetails.objects.get_or_create(user=u)[0])
