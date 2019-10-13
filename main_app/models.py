from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class Unit(models.Model):
    name = models.TextField()
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)  # grams everywhere

    objects = models.Manager()


class Ingredient(models.Model):
    name = models.CharField(max_length=80, unique=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    units = models.ManyToManyField(Unit, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class CookingTool(models.Model):
    name = models.CharField(max_length=80)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    recipe_text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
    )
    tools = models.ManyToManyField(CookingTool)
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    average_rating = models.FloatField(default=0)
    times_rated = models.IntegerField(default=0)
    objects = models.Manager()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)

    objects = models.Manager()


@receiver(pre_delete, sender=Ingredient)
def delete_related_recipes(sender, instance, using, **kwargs):
    for recipe in Ingredient.objects.get(id=instance.id).recipe_set.all():
        recipe.delete()
