from main_app.models import *


class TestDatabase:
    @classmethod
    def create_custom_test_database(cls, ingredient_data=None, dish_data=None):
        if ingredient_data:
            Ingredient.objects.bulk_create(
                [Ingredient(name=n[0], price=n[1], is_vegetarian=n[2], is_vegan=n[3], is_gluten_free=n[4]) for n in
                 ingredient_data])
        if dish_data:
            for n in dish_data:
                d = Dish(name=n[0], description=n[1], image="default.png")
                d.save()
                for ing_name in n[2]:
                    d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    @classmethod
    def create_default_test_database(cls):
        ingredient_data = [
            ("Water", 2, True, True, True),
            ("Lemon", 8, True, True, True)

        ]
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        cls.create_custom_test_database(ingredient_data=ingredient_data,dish_data=dish_data)
