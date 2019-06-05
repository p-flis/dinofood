from main_app.models import *


class TestDatabase:
    @classmethod
    def create_custom_test_database(cls, *, unit_data=None, ingredient_data=None, tool_data=None, recipe_data=None):
        if unit_data:
            Unit.objects.bulk_create([Unit(name=n[0], amount=n[1]) for n in unit_data])
        if ingredient_data:
            Ingredient.objects.bulk_create(
                [Ingredient(name=n[0],
                            price=n[1],
                            is_vegetarian=n[2],
                            is_vegan=n[3],
                            is_gluten_free=n[4])
                 for n in ingredient_data])
        if recipe_data:
            for n in recipe_data:
                recipe_model = Recipe(name=n[0], description=n[1], image="default.png")
                recipe_model.save()
                for ing_name in n[2]:
                    recipe_model.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    @classmethod
    def create_default_test_database(cls):

        ingredient_data = [
            ("Water", 2, True, True, True),
            ("Lemon", 8, True, True, True)

        ]
        recipe_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        cls.create_custom_test_database(ingredient_data=ingredient_data,recipe_data=recipe_data)
