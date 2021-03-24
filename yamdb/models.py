from django.db import models
from django.contrib.auth.models import (PermissionsMixin,
                                        AbstractBaseUser,
                                        BaseUserManager)

class UserAccountManager(BaseUserManager):
    def create_user(self, email, role, username, password):
        user = self.model(
            email=email, role=role, username=username, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, username, password):
        user = self.create_user(
            email=email, role=role, username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username_):
        print(username_)
        return self.get(username=username_)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=40, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=40, unique=True)
    role = models.CharField(
        max_length=30, verbose_name='role', default='user', null=True, blank=True)
    description = models.TextField(
        max_length=100, verbose_name='description', null=True, blank=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'email']

    objects = UserAccountManager()

    def get_short_name(self):
        return str(self.username)

    def natural_key(self):
        return str(self.username)

    def __str__(self):
        return str(self.username)
