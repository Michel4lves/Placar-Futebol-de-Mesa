from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, cpf, password, **extra_fields):
        """
        Create and save a user with the given CPF and password.
        """
        if not cpf:
            raise ValueError("The given username must be set")
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, cpf=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(cpf, password, **extra_fields)

    def create_superuser(self, cpf=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(cpf, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    App base User class.

    Cpf and password are required. Other fields are optional.
    """
    cpf_validator = RegexValidator(
        regex=r'^\d{11}$',
        message=_("CPF must be exactly 11 digits without punctuation."),
    )

    cpf = models.CharField(
        _("CPF"),
        max_length=11,
        unique=True,
        validators=[cpf_validator],
        help_text=_("Enter your 11-digit CPF without punctuation."),
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    nickname = models.CharField(_("nickname"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True, null=True)
    association = models.ForeignKey("Associate", on_delete=models.SET_NULL, null=True, blank=True)
    birth_year = models.PositiveIntegerField(_("year of birth"), null=True, blank=True)
    category = models.CharField(_("category"), max_length=50, blank=True)
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
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the nickname or short name for the user."""
        return self.nickname if self.nickname != '' else self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Going to email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def save(self, *args, **kwargs):
    #     """Automatically set the category based on birth year."""
    #     if self.birth_year:
    #         current_year = timezone.now().year
    #         age = current_year - self.birth_year
    #         if age < 50:
    #             self.category = "Free"
    #         elif 50 <= age < 60:
    #             self.category = "Senior"
    #         else:
    #             self.category = "Master"
    #     super().save(*args, **kwargs)


class Associate(models.Model):
    """Model for associations."""
    acronym = models.CharField(_("acronym"), max_length=20)
    name = models.CharField(_("name"), max_length=150)
    logo = models.ImageField(_("logo"), upload_to="logos/", blank=True, null=True)

    class Meta:
        verbose_name = "Associação"  # Nome no singular
        verbose_name_plural = "Associações"  # Nome no plural

    def __str__(self):
        return self.name
