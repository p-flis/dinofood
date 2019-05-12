from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db.models import Count, Sum, F

from base.models import *

# https://github.com/taranjeet/django-library-app/blob/master/djlibrary/templates/store/create_normal.html


# Create your views here.


def recipe_search(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        return render(request, "food/search_recipe.html", {"ingredients": ingredients})
    elif request.method == 'POST':
        data = request.POST.copy()
        ingredients_in_fridge = data.getlist("ingredients_in_fridge")
        ingredients_in_recipe = data.getlist("ingredients_in_recipe")
        extra_money = data.get("extra_money")

        ingredients_in_recipe_len = len(ingredients_in_recipe)

        # recipes_affordable = recipes_with_required_ings.exclude(ingredients__name__in=ingredients_in_fridge)
        recipes_not_affordable = Dish.objects\
            .exclude(ingredients__name__in=ingredients_in_fridge)\
            .annotate(recipe_price=Sum(F('dishdetails__quantity')*F('dishdetails__ingredient__price')))\
            .filter(recipe_price__gt=extra_money)
        ids_not_affordable = [item.id for item in recipes_not_affordable.all()]
        recipes_affordable = Dish.objects.exclude(id__in=ids_not_affordable)

        recipes_with_required_ings = recipes_affordable \
            .filter(ingredients__name__in=ingredients_in_recipe) \
            .annotate(ing_num=Count('ingredients')) \
            .filter(ing_num=ingredients_in_recipe_len)

        return render(request, "food/recipe.html", {"list_items": recipes_with_required_ings.all()})





