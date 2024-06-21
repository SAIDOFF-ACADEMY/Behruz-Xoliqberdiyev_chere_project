from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import BaseModel


class User(AbstractUser, BaseModel):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, unique=True)
    email = models.EmailField('email', unique=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserContactApplication(BaseModel):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'User Contact Application'
        verbose_name_plural = 'User Contact Applications'
