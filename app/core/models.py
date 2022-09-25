from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin )

class MyUserManager(BaseUserManager):
    """object manager for user"""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user =  self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            return ValueError("Email must be provided")
        email = self.normalize_email(email)

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("superuser must be a staff")
        if not extra_fields.get("is_superuser"):
            raise ValueError("superuser must be a superuser")
        if not extra_fields.get("is_active"):
            return ValueError("Superuser must be active")

        user = self.create_user(email, password, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User Model"""
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = MyUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
