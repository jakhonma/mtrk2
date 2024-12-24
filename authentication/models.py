from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import Group, PermissionsMixin, AbstractBaseUser, Permission
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from authentication.managers import UserManager, AdminManager, LeaderManager, EmployeeManager, LowUserManager
from utils.choices import UserRoleEnum


class User(AbstractBaseUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        ADMIN = 'ADMIN', 'ADMIN'
        LEADER = 'LEADER', 'LEADER'
        EMPLOYEE = 'EMPLOYEE', 'EMPLOYEE'
        LOW_USER = 'LOW_USER', 'LOW_USER'

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
    role = models.CharField(
        max_length=10,
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
        self.type = UserRoleEnum.ADMIN
        return super().save(*args, **kwargs)


class LeaderUser(User):
    class Meta:
        proxy = True
        verbose_name = _("leader")
        verbose_name_plural = _("leaders")

    objects = LeaderManager()

    def save(self, *args, **kwargs):
        self.type = UserRoleEnum.LEADER
        return super().save(*args, **kwargs)


class EmployeeUser(User):
    class Meta:
        proxy = True
        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    objects = EmployeeManager()

    def save(self, *args, **kwargs):
        self.type = UserRoleEnum.EMPLOYEE
        return super().save(*args, **kwargs)


class LowUser(User):
    class Meta:
        proxy = True
        verbose_name = _("low user")
        verbose_name_plural = _("low user")

    objects = LowUserManager()

    def save(self, *args, **kwargs):
        self.type = UserRoleEnum.LOW_USER
        return super().save(*args, **kwargs)
