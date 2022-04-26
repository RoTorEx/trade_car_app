from django.apps import apps
from django.db import models
from django.core.mail import send_mail
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, UserManager  # , User
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_("email address"), blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_buyer = models.BooleanField(
        _("buyer status"),
        default=False,
        help_text=_("Indicates whether the user is a car buyer."),
    )

    is_dealership = models.BooleanField(
        _("dealership status"),
        default=False,
        help_text=_("Indicates if the user is a car dealer."),
    )

    is_supplier = models.BooleanField(
        _("supplier status"),
        default=False,
        help_text=_("Indicates if the user is an auto supplier."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        # abstract = True
        # swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
