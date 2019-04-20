from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Dishes(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    recipe = models.TextField()

class Categories(models.Model):
    name = models.CharField(max_length=80)


class Ingredients(models.Model):
    name = models.CharField(max_length=80)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

class DishesDetails(models.Model):
    dish = models.ForeignKey(Dishes,on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=80)

class Users(models.Model):
    nick = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    admin = models.BooleanField(default=False)


class Ratings(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True,null=True)
    favourite = models.BooleanField(default=False)

