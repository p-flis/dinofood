from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404

from base.models import *


def recipe(request):
    dishes = Dish.objects.all()
    return render(request, "food/recipe.html", {"list_items": dishes})

@login_required(login_url='/accounts/login')
def add_recipe(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        return render(request, "food/new_recipe_form.html", {"ingredients": ingredients})
    elif request.method == 'POST':
        data = request.POST.copy()
        print(data)
        d = Dish(name=data["name"], description=data["description"], recipe=data["recipe"])
        d.save()
        # print(data["ingredients"])
        # print(data.get("ingredients"))
        # print(data.getlist("ingredients"))
        # i_list = Ingredient.objects.filter(name__in=data.getlist("ingredients")).all()
        i_list = [Ingredient.objects.get(name=ing) for ing in data.getlist("ingredients")]
        q_list = data.getlist("quantities")
        for i in range(len(i_list)):
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
    if not dish:
        raise Http404
    return render(request, "food/recipe_id_get.html", {"item": dish.get(id=dish_id)})

@login_required(login_url='/accounts/login') #TODO: change to checking ownership
def recipe_id_delete(request, dish_id):
    dish = Dish.objects.filter(id=dish_id)
    if not dish:
        raise Http404
    dish.delete()
    return redirect('/recipe')
