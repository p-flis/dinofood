from django.shortcuts import render, redirect
from django.http import Http404

from base.models import *


def ingredient(request):
    ingredients = Ingredient.objects.all()
    return render(request, "food/ingredients.html", {"list_items": ingredients})


def add_ingredient(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        if not categories:
            return render(request, "food/no_categories.html")
        # print(categories)
        return render(request, "food/new_ingredient_form.html", {"categories": categories})
    elif request.method == 'POST':
        data = request.POST.copy()
        # print(data)
        d = Ingredient(name=data["name"], price=data["price"])
        c = Category.objects.get(name=data.get("categories"))
        d.category = c
        d.save()
        return redirect('/ingredient')


def ingredient_id(request, ing_id):
    ing = Ingredient.objects.filter(id=ing_id)
    if not ing:
        raise Http404
    return render(request, "food/ingredient_id_get.html", {"item": ing.get(id=ing_id)})


def ingredient_id_delete(request, ing_id):
    ing = Ingredient.objects.filter(id=ing_id)
    if not ing:
        raise Http404
    ing.delete()
    return redirect('/ingredient')