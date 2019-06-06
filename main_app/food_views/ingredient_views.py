from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from main_app.forms import IngredientForm
from main_app.models import *
import json


def ingredient(request):
    ingredients = Ingredient.objects.all()
    return render(request, "food/ingredients.html", {"list_items": ingredients})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_ingredient(request):
    if request.method == 'GET':
        form = IngredientForm()
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
        # else:
        #     print('Invalid add ingredient form')
        #     print('reasons: ')
        #     for reason in form.errors:
        #         print(reason)
        #         for error in form.errors[reason]:
        #             print(error)
        return redirect('/ingredient')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_ingredient_to_default(request):
    if request.method == 'GET':
        form = IngredientForm()
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            file_name = "default_db.json"
            with open(file_name, 'r', encoding='utf-8') as file:
                db = json.load(file)
                ingredients_data = db['ingredients']
                ingredients_data.append({"name": form.cleaned_data["name"],
                                         "price": int(form.cleaned_data["price"])})
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(db, file)
        return redirect('/ingredient')


def ingredient_id(request, object_id):
    ing = Ingredient.objects.filter(id=object_id)
    if not ing:
        raise Http404
    return render(request, "food/ingredient_id_get.html", {"item": ing.get(id=object_id)})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def ingredient_id_delete(request, object_id):
    ing = Ingredient.objects.filter(id=object_id)
    if not ing:
        raise Http404
    ing = ing.get()
    ing.delete()
    return redirect('/ingredient')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def ingredient_id_update(request, object_id):
    if request.method == 'GET':
        ing = Ingredient.objects.filter(id=object_id)
        if not ing:
            raise Http404
        ing = ing.get()
        form = IngredientForm(instance=ing)
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        instance = Ingredient.objects.get(id=object_id)
        form = IngredientForm(instance=instance,data=request.POST)
        if form.is_valid():
            form.save()
        # else:
        #     print('Invalid update ingredient form')
        #     print('reasons: ')
        #     for reason in form.errors:
        #         print(reason)
        #         for error in form.errors[reason]:
        #             print(error)

        return redirect('/ingredient')
