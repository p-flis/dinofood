from django.db import models
from accounts import models as accounts_models
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class Ingredient(models.Model):
    name = models.CharField(max_length=80, unique=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    objects = models.Manager()


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Dish(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    recipe = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='DishIngredient',
        through_fields=('dish', 'ingredient'),
    )
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)

    objects = models.Manager()


class DishIngredient(models.Model):
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
