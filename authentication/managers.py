from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from utils.choices import UserRole


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(
            username=username,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class AdminManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
            role=UserRole.ADMIN,
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        return queryset


class ArchiveDirectorManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
            role=UserRole.ARCHIVE_DIRECTOR,
            is_superuser=False,
            is_active=True,
            is_staff=False
        )
        return queryset


class ChannelDirectorManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
            role=UserRole.CHANNEL_DIRECTOR,
            is_superuser=False,
            is_active=True,
            is_staff=False
        )
        return queryset


class ChannelAssistantManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
            role=UserRole.CHANNEL_ASSISTANT,
            is_superuser=False,
            is_active=True,
            is_staff=False
        )
        return queryset


class ArchiveEmployeeManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
            role=UserRole.ARCHIVE_EMPLOYEE,
            is_superuser=False,
            is_active=True,
            is_staff=False
        )
        return queryset


class ChannelEmployeeManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
            role=UserRole.CHANNEL_EMPLOYEE,
            is_superuser=False,
            is_active=True,
            is_staff=False
        )
        return queryset


class LowUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
            role=UserRole.LOW_USER,
            is_superuser=False,
            is_active=True,
            is_staff=False
        )
        return queryset
