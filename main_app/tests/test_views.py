from django.shortcuts import render
import json
from main_app.tests.TestSetupDatabase import *

from main_app.models import *
from accounts.models import *


def empty_database():
    Recipe.objects.all().delete()
    Ingredient.objects.all().delete()
    Unit.objects.all().delete()
    CookingTool.objects.all().delete()
    # User.objects.all().delete() #idk where it is and if it is safe to remove users
    RecipeIngredient.objects.all().delete()
    Rating.objects.all().delete()


def load_db_from_json(file_name):
    with open(file_name, encoding='utf-8') as file:
        db = json.load(file)

        TestDatabase.create_custom_test_database(units_data=db['units'],
                                                 ingredients_data=db['ingredients'],
                                                 tools_data=db['tools'],
                                                 recipes_data=db['recipes'])


def test_empty_database(request):
    empty_database()
    return render(request, "empty_database.html")


def test_default_database(request):
    empty_database()

    load_db_from_json("default_db.json")

    return render(request, "default_database.html")


def save_database_to_default(request):
    units_data = [
        {
            'name': unit_object.name,
            'amount': int_from_decimal(unit_object.amount)
        }
        for unit_object in Unit.objects.all()
    ]
    tools_data = [
        {
            'name': tool_object.name
        }
        for tool_object in CookingTool.objects.all()
    ]
    ingredients_data = [
        {
            'name': ingredient_object.name,
            'price': int_from_decimal(ingredient_object.price),
            'units': [
                {
                    'name': unit_object.name
                }
                for unit_object in ingredient_object.units.all()
            ]
        }
        for ingredient_object in Ingredient.objects.all()
    ]
    recipes_data = [
        {
            'name': recipe_object.name,
            'description': recipe_object.description,
            'recipe': recipe_object.recipe,
            'ingredients': [
                {
                    'name': recipeingredient_object.ingredient.name,
                    'quantity': recipeingredient_object.quantity,
                    'unit': recipeingredient_object.unit.name if recipeingredient_object.unit else "Gram"
                }
                for recipeingredient_object in recipe_object.recipeingredient_set.all()
            ],
            'image': recipe_object.image.name if recipe_object.image else ""
        }
        for recipe_object in Recipe.objects.all()
    ]
    db = {
        'units': units_data,
        'ingredients': ingredients_data,
        'tools': tools_data,
        'recipes': recipes_data,
    }
    file_name = "default_db.json"
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(db, file)

    return render(request, "default_database.html")
