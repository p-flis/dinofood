from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db.models import Count

from .models import *

# https://github.com/taranjeet/django-library-app/blob/master/djlibrary/templates/store/create_normal.html


# Create your views here.
def recipe(request):
    dishes = Dish.objects.all()

    return render(request, "food/recipe.html", {"itemlist": dishes})


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
        #i_list = Ingredient.objects.filter(name__in=data.getlist("ingredients")).all()
        i_list = [Ingredient.objects.get(name=ing) for ing in data.getlist("ingredients")]
        q_list = data.getlist("quantities")
        for i in range(1,len(i_list)):
            try:
                q = int(q_list[i])
                d.ingredients.add(i_list[i], through_defaults={'quantity': q})
            except ValueError:
                pass
           
        d.save()
        return redirect('/recipe')
    raise Http404


def recipe_id(request, dish_id):
    dish = Dish.objects.filter(id=dish_id)
    return render(request, "food/recipe_id_get.html", {"item": dish.get(id=dish_id)})


def recipe_id_delete(request, dish_id):
    dish = Dish.objects.filter(id=dish_id)
    dish.delete()
    return redirect('/recipe')


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
        return render(request, "food/recipe.html", {"itemlist": d.all()})


def ingredient(request):
    ingredients = Ingredient.objects.all()
    return render(request, "food/ingredients.html", {"itemlist": ingredients})


def add_ingredient(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        if not categories:
            return render(request, "food/no_categories.html")
        print(categories)
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
    return render(request, "food/ingredient_id_get.html", {"item": ing.get(id=ing_id)})


def ingredient_id_delete(request, ing_id):
    ing = Ingredient.objects.filter(id=ing_id)
    ing.delete()
    return redirect('/ingredients')


def category(request):
    categories = Category.objects.all()
    return render(request, "food/category.html", {"itemlist": categories})


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
    return render(request, "food/category_id_get.html", {"item": cat.get(id=cat_id)})


def category_id_delete(request, cat_id):
    cat = Category.objects.filter(id=cat_id)
    cat.delete()
    return redirect('/category')
