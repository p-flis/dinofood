from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db.models import Count

from base.models import *

# https://github.com/taranjeet/django-library-app/blob/master/djlibrary/templates/store/create_normal.html


# Create your views here.


def recipe_search(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        return render(request, "food/search_recipe.html", {"ingredients": ingredients})
    elif request.method == 'POST':
        data = request.POST.copy()
        ings = data.getlist("ingredients")
        lin = len(ings)
        d = Dish.objects\
            .filter(ingredients__name__in=ings)\
            .annotate(ing_num=Count('ingredients'))\
            .filter(ing_num=lin)
        return render(request, "food/recipe.html", {"list_items": d.all()})





