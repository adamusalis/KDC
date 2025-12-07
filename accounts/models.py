from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# 1. The Custom Manager (Teaches Django how to create users without usernames)
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, email, password, **extra_fields)

# 2. The Custom User Model
class CustomUser(AbstractUser):
    username = None  # Remove username
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
   
    # VTU Specific Fields
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_pin = models.CharField(max_length=4, blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    # Link the Manager to the User
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number