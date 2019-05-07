from django.db import models

class User(models.Model):
    nick = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    admin = models.BooleanField(default=False)
