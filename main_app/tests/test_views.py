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
    Dish.objects.all().delete()
    Ingredient.objects.all().delete()
    # User.objects.all().delete() #idk where it is and if it is safe to remove users

    # two of above should be enough if relations were configured properly
    # but now it is safer to delete everything

    DishDetails.objects.all().delete()
    Rating.objects.all().delete()


def load_db_from_json(file_name):
    with open(file_name, encoding='utf-8') as file:
        db = json.load(file)

        ingredients_data = db['ingredients']
        Ingredient.objects.bulk_create([Ingredient(name=ingredient_data['name'],
                                                   price=ingredient_data['price'])
                                        for ingredient_data in ingredients_data])

        recipes_data = db['recipes']
        for recipe_data in recipes_data:
            d = Dish(name=recipe_data['name'], description=recipe_data['description'], recipe=recipe_data['recipe'])
            d.save()
            for ingredient_data in recipe_data['ingredients']:
                d.ingredients.add(Ingredient.objects.get(name=ingredient_data['name']),
                                  through_defaults={'quantity': ingredient_data['quantity']})


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
