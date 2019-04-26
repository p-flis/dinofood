from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .models import *

# https://github.com/taranjeet/django-library-app/blob/master/djlibrary/templates/store/create_normal.html


# Create your views here.
def recipe(request):
    dishes = Dish.objects.all()

    return render(request, "food/recipe.html", {"dishes": dishes})


def add_recipe(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        return render(request, "food/new_recipe_form.html", {"ingredients": ingredients})
    elif request.method == 'POST':
        data = request.POST.copy()
        print(data)
        d = Dish(name=data["name"], description=data["description"])
        d.save()
        # print(data["ingredients"])
        # print(data.get("ingredients"))
        # print(data.getlist("ingredients"))
        i_list = Ingredient.objects.filter(name__in=data.getlist("ingredients")).all()
        for i in i_list:
            d.ingredients.add(i, through_defaults={'quantity': 1})
        d.save()
        return redirect('/recipe')
    raise Http404


def recipe_id(request, dish_id):
    dish = Dish.objects.filter(id=dish_id)
    if request.method == 'GET':
        return render(request, "food/recipe_id_get.html", {"recipe": dish.get(id=dish_id)})
    elif request.method == 'POST':
        dish.delete()
        return redirect('/recipe')
    raise Http404


def ingredient(request):
    ingredients = Ingredient.objects.all()

    return render(request, "food/ingredients.html", {"ingredients": ingredients})


def add_ingredient(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, "food/new_ingredient_form.html", {"categories": categories})
    elif request.method == 'POST':
        data = request.POST.copy()
        print(data)
        d = Ingredient(name=data["name"], price=data["price"])
        c = Category.objects.get(name=data.get("categories"))
        d.category = c
        d.save()
        return redirect('/ingredient')


def ingredient_id(request, ing_id):
    ing = Ingredient.objects.filter(id=ing_id)
    if request.method == 'GET':
        return render(request, "food/ingredient_id_get.html", {"ingredient": ing.get(id=ing_id)})
    elif request.method == 'POST':
        ing.delete()
        return redirect('/ingredients')
    raise Http404


def category(request):
    categories = Category.objects.all()

    return render(request, "food/category.html", {"categories": categories})


def add_category(request):
    if request.method == 'GET':
        return render(request, "food/new_category_form.html")
    elif request.method == 'POST':
        data = request.POST.copy()
        print(data)
        c = Category(name=data["name"])
        c.save()
        return redirect('/category')
    raise Http404


def category_id(request, cat_id):
    cat = Category.objects.filter(id=cat_id)
    if request.method == 'GET':
        return render(request, "food/category_id_get.html", {"recipe": cat.get(id=cat_id)})
    elif request.method == 'POST':
        cat.delete()
        return redirect('/recipe')
    raise Http404
