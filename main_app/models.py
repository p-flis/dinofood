from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete

class Unit(models.Model):
    name = models.TextField()
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2) #grams everywhere
    objects = models.Manager()

class Ingredient(models.Model):
    name = models.CharField(max_length=80, unique=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    units = models.ManyToManyField(
        Unit,
        through='IngredientUnit',
        through_fields=('ingredient', 'unit'),
    )
    objects = models.Manager()

class IngredientUnit(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING)
    objects = models.Manager()


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)

class CookingTool(models.Model):
    name = models.CharField(max_length=80)
    objects = models.Manager()

class Dish(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    recipe = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='DishIngredient',
        through_fields=('dish', 'ingredient'),
    )
    tools = models.ManyToManyField(
        CookingTool,
        through='DishCookingTool',
        through_fields=('dish', 'tool'),
    )
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    accepted = models.BooleanField(default=False)

    objects = models.Manager()

class DishCookingTool(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    tool = models.ForeignKey(CookingTool, on_delete=models.CASCADE)
    objects = models.Manager()

class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)
    objects = models.Manager()





@receiver(pre_delete, sender=Ingredient)
def delete_related_recipes(sender, instance, using, **kwargs):
    for recipe in Ingredient.objects.get(id=instance.id).dish_set.all():
        recipe.delete()
