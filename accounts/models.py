from django.db import models
from django.contrib.auth.models import AbstractUser
from main_app import models as main_models


class User(AbstractUser):
    nick = models.CharField(max_length=30)
    admin = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(main_models.Ingredient)
    tools = models.ManyToManyField(main_models.CookingTool)
    ratings = models.ManyToManyField(
        main_models.Recipe,
        through='Rating',
        through_fields=('user', 'recipe'),
    )

    def __str__(self):
        return self.email


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(main_models.Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    favourite = models.BooleanField(default=False)
    objects = models.Manager()
