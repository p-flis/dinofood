from django.db import models
from accounts import models as accounts_models
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    objects = models.Manager()


class Ingredient(models.Model):
    name = models.CharField(max_length=80, unique=True)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    objects = models.Manager()


class Dish(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    recipe = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='DishDetails',
        through_fields=('dish', 'ingredient'),
    )

    objects = models.Manager()


class DishDetails(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    objects = models.Manager()


class Rating(models.Model):
    user = models.ForeignKey(accounts_models.User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    favourite = models.BooleanField(default=False)

    objects = models.Manager()


@receiver(pre_delete, sender=Ingredient)
def delete_related_recipes(sender, instance, using, **kwargs):
    for recipe in Ingredient.objects.get(id=instance.id).dish_set.all():
        recipe.delete()
