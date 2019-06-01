from django.db import models
from django.contrib.auth.models import AbstractUser
from main_app import models as main_models

class User(AbstractUser):
    nick = models.CharField(max_length=30)
    admin = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(
        main_models.Ingredient,
        through='UserIngredient',
        through_fields=('user', 'ingredient'),
    )
    tools = models.ManyToManyField(
        main_models.CookingTool,
        through='UserCookingTool',
        through_fields=('user', 'tool'),
    )

    def __str__(self):
        return self.email

class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(main_models.Ingredient, on_delete=models.CASCADE)
    objects = models.Manager()

class UserCookingTool(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(main_models.CookingTool, on_delete=models.CASCADE)
    objects = models.Manager()

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(main_models.Dish, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    favourite = models.BooleanField(default=False)
    objects = models.Manager()
