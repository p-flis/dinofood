from main_app.models import *


class TestDatabase:
    @classmethod
    def create_default_test_database(cls):
        ingredient_data = [
            ("Water", 2),
            ("Lemon", 8)

        ]
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1]) for n in ingredient_data])
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    @classmethod
    def create_custom_test_database(cls, ingredient_data=[], dish_data=[]):
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1]) for n in ingredient_data])
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})
