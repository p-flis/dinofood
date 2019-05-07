from django.db import models


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=80)


class Ingredient(models.Model):
    name = models.CharField(max_length=80)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Dish(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    recipe = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='DishDetails',
        through_fields=('dish', 'ingredient'),
    )


class DishDetails(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()



class Rating(models.Model):
    user = models.ForeignKey(accounts.User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True,null=True)
    favourite = models.BooleanField(default=False)
