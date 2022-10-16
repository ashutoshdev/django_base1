from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import jsonfield
from oauth2_provider.models import Application, AccessToken

from base.models import AbstractModel
from pos_users.managers import UserManager


class Organization(AbstractModel):
    """
	Organization Definition
	Enable 2-factor authentication as business profile level choice
	"""
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address = jsonfield.JSONField()
    tax_number = models.CharField(max_length=10, null=True, blank=True)
    is_operational = models.BooleanField(default=True)
    is_2factor_auth_required = models.BooleanField(default=False)

    def __str__(self):
        return u'%s' % self.company_name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = 'Organizations'
        db_table = 'organization'


class User(AbstractBaseUser, AbstractModel, PermissionsMixin):
    """
    All type of users setup and profile
    Login by email id and password
    optional by OTP verification login can be enabled
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserManager()

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return u'%s' % self.email

    def create_oauth_application(self):
        return Application.objects.create(
            user=User(id=self.id),
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD)

    def application_details(self):
        app = Application.objects.get(user=User(id=self.id), )
        return {"client_id": app.client_id, "client_secret": app.client_secret}

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'


class OrganizationUser(AbstractModel):
    """
	Business specific users
	"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='organization_user')
    phone_number = models.CharField(max_length=20, null=True, blank=True,
                                    help_text="Please include country code.")
    email_verified = models.BooleanField(default=False)
    is_business_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return u'%s - %s' % (self.user, self.phone_number)

    class Meta:
        verbose_name = 'Organization User'
        verbose_name_plural = 'Organization Users'
        db_table = 'organization_user'
