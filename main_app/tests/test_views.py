from django.shortcuts import render
import json

from main_app.models import *
from accounts.models import *


def int_from_decimal(number):
    return float(number)


def decimal_from_int(number):
    return number


def empty_database():
    Dish.objects.all().delete()
    Ingredient.objects.all().delete()
    Unit.objects.all().delete()
    CookingTool.objects.all().delete()
    # User.objects.all().delete() #idk where it is and if it is safe to remove users
    DishIngredient.objects.all().delete()
    Rating.objects.all().delete()


def load_db_from_json(file_name):
    with open(file_name, encoding='utf-8') as file:
        db = json.load(file)

        units_data = db['units']
        Unit.objects.bulk_create([Unit(name=unit_data['name'],
                                       amount=decimal_from_int(unit_data['amount']))
                                  for unit_data in units_data])

        ingredients_data = db['ingredients']
        for ingredient_data in ingredients_data:
            ingredient_model = Ingredient(name=ingredient_data['name'],
                                          price=decimal_from_int(ingredient_data['price']))
            ingredient_model.save()
            for unit_data in ingredient_data['units']:
                ingredient_model.units.add(Unit.objects.get(name=unit_data['name']))

        tools_data = db['tools']
        CookingTool.objects.bulk_create([CookingTool(name=tool_data['name'])
                                         for tool_data in tools_data])

        recipes_data = db['recipes']
        for recipe_data in recipes_data:
            recipe_model = Dish(name=recipe_data['name'],
                                description=recipe_data['description'],
                                recipe=recipe_data['recipe'])
            if ("image" in recipe_data) and recipe_data['image'] != "":
                recipe_model.image = recipe_data['image']
            recipe_model.save()
            for ingredient_data in recipe_data['ingredients']:
                ingredient_model = Ingredient.objects.get(name=ingredient_data['name'])
                unit_model = ingredient_model.units.get(name=ingredient_data['unit'])
                recipe_model.ingredients.add(ingredient_model,
                                             through_defaults={'quantity': ingredient_data['quantity'],
                                                               'unit': unit_model})
            if 'tools' in recipe_data:
                for tool_data in recipe_data['tools']:
                    recipe_model.tools.add(CookingTool.objects.get(name=tool_data['name']))


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
                    'name': dishingredient_object.ingredient.name,
                    'quantity': dishingredient_object.quantity,
                    'unit': dishingredient_object.unit.name if dishingredient_object.unit else "Gram"
                }
                for dishingredient_object in recipe_object.dishingredient_set.all()
            ],
            'image': recipe_object.image.name if recipe_object.image else ""
        }
        for recipe_object in Dish.objects.all()
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
