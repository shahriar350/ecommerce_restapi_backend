from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from rest_framework.authtoken.models import Token

from admin_app.models import ShopCategory


class CustomUserManager(BaseUserManager):
    def create_user(self, name, phone_number, password, **extra_fields):
        if Users.objects.filter(phone_number=phone_number).count() > 0:
            raise ValidationError(_('Phone number is already taken'))
        if not phone_number:
            raise ValidationError(_('Phone number is required'))
        if len(phone_number) != 11:
            raise ValidationError(_('Phone number must be 11 number'))
        if phone_number[0] != '0' and phone_number[1] != '1':
            raise ValidationError(_('Phone number must be start with 01'))
        if not password:
            raise ValidationError(_('Password is required'))
        if not phone_number.isnumeric():
            raise ValidationError(_('Phone number must be numeric'))
        extra_fields.setdefault("active", True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.last_login = timezone.now()
        user.name = name.title()
        user.save(using=self._db)
        return user

    def create_seller(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault('seller', True)
        extra_fields.setdefault('active', True)
        if extra_fields.get('seller') is not True:
            raise ValueError(_('Seller must be true'))
        return self.create_user(name, phone_number, password, **extra_fields)

    def create_superuser(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("admin", True)
        extra_fields.setdefault("active", True)
        user = self.create_user(name, phone_number, password, **extra_fields)
        return user


class Users(AbstractBaseUser):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    name = models.CharField(_('Your name'), max_length=100,
                            validators=[
                                RegexValidator(
                                    regex=r'^[a-zA-Z ]*$',
                                    message=_('name must be Alpha'),
                                ),
                            ]
                            )
    phone_number = models.CharField(_('Phone number'), max_length=11, unique=True)
    admin = models.BooleanField(default=False)
    seller = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_seller(self):
        return self.seller

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin


class SellerRequest(models.Model):
    seller_name = models.CharField(_('Seller name'), max_length=100, blank=False, null=False)
    shop_name = models.CharField(_('Shop name'), max_length=100, blank=False, null=False)
    contact_location = models.CharField(_('Contact location'), max_length=100, blank=False, null=False)
    contact_number = models.CharField(_('Contact number'), max_length=11, unique=True,
                                      primary_key=True)
    shop_business_address = models.TextField(_("Shop business address"))
    category_option = models.ForeignKey(ShopCategory, on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
    accept_by = models.ForeignKey(Users, on_delete=models.CASCADE, limit_choices_to={'admin': True}, null=True,
                                  blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
