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

        search_result = Dish.objects

        if ingredients_in_fridge and any(ingredients_in_fridge):
            search_result = search_result \
                .exclude(ingredients__name__in=ingredients_in_fridge)\

        print(search_result.all())

        search_result = search_result\
            .annotate(recipe_price=Sum(F('dishdetails__quantity') * F('dishdetails__ingredient__price'))) \
            .filter(recipe_price__gt=extra_money)

        print(search_result.all())
        # print(search_result.query)
        ids_not_affordable = [item.id for item in search_result.all()]
        search_result = Dish.objects.exclude(id__in=ids_not_affordable)

        if ingredients_in_recipe and any(ingredients_in_recipe):
            search_result = search_result \
                .filter(ingredients__name__in=ingredients_in_recipe) \
                .annotate(ing_num=Count('ingredients')) \
                .filter(ing_num=ingredients_in_recipe_len)

        # print(search_result.query)
        return render(request, "food/recipe.html", {"list_items": search_result.all()})





