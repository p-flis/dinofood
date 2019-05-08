from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nick = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    admin = models.BooleanField(default=False)
    def __str__(self):
        return self.email
