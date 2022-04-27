from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager  # , User
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    ROLE = (
        ('staff', 'Staff'),
        ('buyer', 'Buyer'),
        ('dealership', 'Dealership'),
        ('supplier', 'Supplier'),
        ('unknown', 'Unknown'))

    username_validator = UnicodeUsernameValidator()

    # Model fields
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

    # role = models.CharField(max_length=15, choices=ROLE)
    role = models.CharField(max_length=15, choices=ROLE, blank=True)

    email = models.EmailField(_("email address"), blank=False)

    verifyed_email = models.BooleanField(default=False)

    # first_name = None
    # last_name = None
    # date_joined = None

    # first_name = models.CharField(_("first name"), max_length=150, blank=True)
    # last_name = models.CharField(_("last name"), max_length=150, blank=True)
    # date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    # Other
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "role"]

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
