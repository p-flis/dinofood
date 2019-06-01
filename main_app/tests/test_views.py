from django.shortcuts import render
import json

from main_app.models import *


# region SearchViews

# endregion

# region DeleteViews


# endregion

# region GetIDViews


# endregion

# region AddViews


# endregion

# region DatabaseTests


def empty_database():
    IngredientUnit.objects.all().delete()
    Dish.objects.all().delete()
    Ingredient.objects.all().delete()
    # User.objects.all().delete() #idk where it is and if it is safe to remove users

    # two of above should be enough if relations were configured properly
    # but now it is safer to delete everything

    DishIngredient.objects.all().delete()
    Rating.objects.all().delete()
    Unit.objects.all().delete()


def load_db_from_json(file_name):
    with open(file_name, encoding='utf-8') as file:
        db = json.load(file)

        units_data = db['units']
        Unit.objects.bulk_create([Unit(name=unit_data['name'],
                                                   amount=unit_data['amount'])
                                        for unit_data in units_data])
        ingredients_data = db['ingredients']
        for ingredient_data in ingredients_data:
            ingred = Ingredient(name=ingredient_data['name'], price=ingredient_data['price'])
            ingred.save()
            for unit_data in ingredient_data['units']:
                ingred.units.add(Unit.objects.get(name=unit_data['name']))

        recipes_data = db['recipes']
        for recipe_data in recipes_data:
            d = Dish(name=recipe_data['name'], description=recipe_data['description'], recipe=recipe_data['recipe'])
            d.save()
            for ingredient_data in recipe_data['ingredients']:
                ingtmp = Ingredient.objects.get(name=ingredient_data['name'])
                u = ingtmp.ingredientunit_set.filter(unit=Unit.objects.get(name=ingredient_data['unit'])).first()
                d.ingredients.add(ingtmp,
                                  through_defaults={'quantity': ingredient_data['quantity'],
                                                    'unit': u.unit})


def test_empty_database(request):
    empty_database()
    return render(request, "empty_database.html")


def test_default_database(request):
    empty_database()

    load_db_from_json("default_db.json")

    return render(request, "default_database.html")


# def load_bcc_from_json(file_name):
#     with open(file_name, encoding='utf-8') as file:
#         db = json.load(file)
#
#         all_category = Category.objects.create(name='ALL')
#         all_category.save()
#
#         for url, recipe_data in db.items():
#             if len(recipe_data['ingredients']) <= 0:
#                 continue
#             if len(recipe_data['title']) >= 75:
#                 recipe_data['title'] = recipe_data['title'][:75] + "..."
#             d = Dish(name=recipe_data['title'],
#                      description=recipe_data['url'] + '\nRecipe from www.bbc.com',
#                      recipe='\n'.join(recipe_data['method']))
#             d.save()
#             ingredients_data = recipe_data['ingredients']
#             for ingredient_data in ingredients_data:
#                 last_digit_id = next((i for i, j in list(enumerate(ingredient_data, 1))[::-1] if j.isdigit()), -1)
#                 if last_digit_id >= 0:
#                     ingredient_data = ingredient_data[ingredient_data.find(' ', last_digit_id) + 1:]
#                 if ingredient_data.find(',') >= 0:
#                     ingredient_data = ingredient_data[:ingredient_data.find(',')]
#                 if Ingredient.objects.filter(name=ingredient_data).exists():
#                     ing = Ingredient.objects.get(name=ingredient_data)
#                 else:
#                     if len(ingredient_data) >= 75:
#                         ingredient_data = ingredient_data[:75] + "..."
#                     ing = Ingredient.objects.create(name=ingredient_data, price=1, category=all_category)
#                     # ing.save()
#                 d.ingredients.add(ing, through_defaults={'quantity': 1})
#
#
# def test_big_database(request):
#     # def test_default_database(request):
#     empty_database()
#
#     load_bcc_from_json("db136.json")
#
#     return render(request, "default_database.html")

# endregion

# region ValidationTests

# endregion

# region AuthorisationTests

# endregion
