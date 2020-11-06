from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import re
from django.core.mail import send_mail
import uuid


# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_("The given user must be set"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self , username, email=None, password=None, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return User


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=150, unique=False,
                                help_text=_("Required"),
                                validators=[validators.RegexValidator(re.compile("^[\w.@+-]+$"),
                                                                      _("Enter a valid username"),
                                                                      _("valid"))])
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), max_length=255, unique=True)
    is_staff = models.BooleanField(_("is staff"), default=False, help_text=_("Designates whether this user can log "
                                                                             "into the admin site "))
    is_active = models.BooleanField(_("is active"), default=True, help_text=_("Designates whether this user should be "
                                                                              "treated  as active "))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    long_id = models.UUIDField(default=uuid.uuid4, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return f"{self.first_name}"

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.username


class UserSystem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    long_id = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.user


class Friend(models.Model):
    user_system = models.ForeignKey(UserSystem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)
    now = timezone.now()
    friendship_day = models.DateTimeField(default=now)
    long_id = models.UUIDField(default=uuid.uuid4, unique=True)


class ReceivedRequest(models.Model):
    user_system = models.ForeignKey(UserSystem, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    now = timezone.now()
    received_day = models.DateTimeField(default=now)
    long_id = models.UUIDField(default=uuid.uuid4, unique=True)
    acepted = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)


class SentRequest(models.Model):
    user_system = models.ForeignKey(UserSystem, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    now = timezone.now()
    sent_day = models.DateTimeField(default=now)
    long_id = models.UUIDField(default=uuid.uuid4, unique=True)
    acepted = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)


class Test(models.Model):
    name = models.BooleanField(default=True)
    long_id = models.UUIDField(default=uuid.uuid4, unique=True)


class Chat(models.Model):
    user_system = models.ForeignKey(UserSystem, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    long_id = models.UUIDField(default=uuid.uuid4, unique=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    long_id = models.UUIDField(default=uuid.uuid4, unique=True)
    now = timezone.now()
    sent_day = models.DateTimeField(default=now)
