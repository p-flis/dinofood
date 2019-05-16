from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from base.forms import IngredientForm
from base.models import *


def ingredient(request):
    ingredients = Ingredient.objects.all()
    return render(request, "food/ingredients.html", {"list_items": ingredients})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_ingredient(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        if not categories:
            return render(request, "food/no_categories.html")
        form = IngredientForm()
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            d = Ingredient(name=form.cleaned_data["name"], price=form.cleaned_data["price"])
            c = Category.objects.get(name=form.cleaned_data['category'])
            d.category = c
            d.save()
        return redirect('/ingredient')


def ingredient_id(request, ing_id):
    ing = Ingredient.objects.filter(id=ing_id)
    if not ing:
        raise Http404
    return render(request, "food/ingredient_id_get.html", {"item": ing.get(id=ing_id)})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def ingredient_id_delete(request, ing_id):
    ing = Ingredient.objects.filter(id=ing_id)
    if not ing:
        raise Http404
    ing.delete()
    return redirect('/ingredient')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def ingredient_id_update(request, ing_id):
    if request.method == 'GET':
        ing = Ingredient.objects.filter(id=ing_id)
        if not ing:
            raise Http404
        item = ing.get(id=ing_id)
        data = {'name': item.name,
                'price': item.price,
                'category': item.category.name}
        form = IngredientForm(data)
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ing = Ingredient.objects.filter(id=ing_id)
            if ing:
                ing.update(name=form.cleaned_data["name"])
                ing.update(price=form.cleaned_data["price"])
                ing.update(category=Category.objects.get(name=form.cleaned_data["category"]))
                # this probably makes 3 changes to the db
            else:
                d = Ingredient(name=form.cleaned_data["name"], price=form.cleaned_data["price"])
                c = Category.objects.get(name=form.cleaned_data["category"])
                d.category = c
                d.save()

        return redirect('/ingredient')
