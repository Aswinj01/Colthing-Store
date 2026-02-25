from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.contrib.auth.models import BaseUserManager

class MyAccountManager(BaseUserManager):

    def create_user(self, first_name="", last_name="", username=None, email=None, password=None):

        if not email:
            raise ValueError("User must have an email address")

        if not username:
            username = email.split("@")[0]

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name or "",   # 🔥 IMPORTANT
            last_name=last_name or "",     # 🔥 IMPORTANT
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user


    def create_superuser(self, first_name="", last_name="", username=None, email=None, password=None):

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    first_name   = models.CharField(max_length=50, blank=True, default="")
    last_name    = models.CharField(max_length=50, blank=True, default="")
    username     = models.CharField(max_length=100, unique=True)
    email        = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, blank=True, default="")

    date_joined  = models.DateTimeField(auto_now_add=True)
    last_login   = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True