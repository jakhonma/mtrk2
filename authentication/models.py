from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import Group, PermissionsMixin, AbstractBaseUser, Permission
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from authentication.managers import (
    UserManager, 
    AdminManager, 
    ArchiveDirectorManager, 
    ChannelDirectorManager, 
    ArchiveEmployeeManager, 
    ChannelAssistantManager,
    ChannelEmployeeManager, 
    LowUserManager
)
from utils.choices import UserRole


class UserRoles(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # is_unique = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

# class UserRole(models.TextChoices):
#         ADMIN = 'ADMIN', 'ADMIN'
#         ARCHIVE_DIRECTOR = 'ARCHIVE_DIRECTOR', 'ARCHIVE_DIRECTOR'
#         CHANNEL_DIRECTOR = 'CHANNEL_DIRECTOR', 'CHANNEL_DIRECTOR'
#         ARCHIVE_EMPLOYEE = 'ARCHIVE_EMPLOYEE', 'ARCHIVE_EMPLOYEE'
#         CHANNEL_ASSISTANT = 'CHANNEL_ASSISTANT', 'CHANNEL_ASSISTANT'
#         CHANNEL_EMPLOYEE = 'CHANNEL_EMPLOYEE', 'CHANNEL_EMPLOYEE'
#         LOW_USER = 'LOW_USER', 'LOW_USER'


class User(AbstractBaseUser, PermissionsMixin):
    

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    full_name = models.CharField(
        _("first name"),
        max_length=200,
        blank=True
    )
    email = models.EmailField(
        _("email address"),
        blank=True
    )
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
    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now
    )
    user_role = models.ForeignKey(
        UserRoles, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    role = models.CharField(
        max_length=18,
        choices=UserRole.choices,
        default=UserRole.LOW_USER,
        blank=True
    )
    groups = models.ForeignKey(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
        on_delete=models.SET_NULL,
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def save(self, *args, **kwargs):
        if not self.pk and not self.is_staff and not self.is_superuser:
            self.password = make_password(self.password)
        return super().save(*args, **kwargs)


class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = _("admin")
        verbose_name_plural = _("admins")

    objects = AdminManager()

    def save(self, *args, **kwargs):
        self.role = UserRole.ADMIN
        return super().save(*args, **kwargs)


class ArchiveDirectorUser(User):
    class Meta:
        proxy = True
        verbose_name = _("archive director")
        verbose_name_plural = _("archive directors")

    objects = ArchiveDirectorManager()

    def save(self, *args, **kwargs):
        self.role = UserRole.ARCHIVE_DIRECTOR
        return super().save(*args, **kwargs)


class ChannelDirectorUser(User):
    class Meta:
        proxy = True
        verbose_name = _("channel director")
        verbose_name_plural = _("channel directors")

    objects = ChannelDirectorManager()

    def save(self, *args, **kwargs):
        self.role = UserRole.CHANNEL_DIRECTOR
        return super().save(*args, **kwargs)


class ChannelAssistantUser(User):
    class Meta:
        proxy = True
        verbose_name = _("channel assistant")
        verbose_name_plural = _("channel assistant")

    objects = ChannelAssistantManager()

    def save(self, *args, **kwargs):
        self.role = UserRole.CHANNEL_ASSISTANT
        return super().save(*args, **kwargs)


class ArchiveEmployeeUser(User):
    class Meta:
        proxy = True
        verbose_name = _("archive employee")
        verbose_name_plural = _("archive employees")

    objects = ArchiveEmployeeManager()

    def save(self, *args, **kwargs):
        self.role = UserRole.ARCHIVE_EMPLOYEE
        return super().save(*args, **kwargs)


class ChannelEmployeeUser(User):
    class Meta:
        proxy = True
        verbose_name = _("channel employee")
        verbose_name_plural = _("channel employees")

    objects = ChannelEmployeeManager()

    def save(self, *args, **kwargs):
        self.role = UserRole.CHANNEL_EMPLOYEE
        return super().save(*args, **kwargs)


class LowUser(User):
    class Meta:
        proxy = True
        verbose_name = _("low user")
        verbose_name_plural = _("low user")

    objects = LowUserManager()

    def save(self, *args, **kwargs):
        self.role = UserRole.LOW_USER
        return super().save(*args, **kwargs)
