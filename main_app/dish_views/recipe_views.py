from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from main_app.forms import RecipeForm
from main_app.models import *
from django.core.mail import send_mail
import json


def recipe(request):
    dishes = Dish.objects.all()
    return render(request, "food/recipe.html", {"list_items": dishes})


@login_required(login_url='/accounts/login')
def add_recipe(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        form = RecipeForm()
        return render(request, "food/new_recipe_form.html", {"ingredients": ingredients, 'form': form})
    elif request.method == 'POST':

        data = request.POST.copy()
        # needed only because of the ingredients not in form but in html
        form = RecipeForm(data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            d = form.save(commit=False)
            d.save()
            i_list = [Ingredient.objects.get(name=ing) for ing in data.getlist("ingredients")]
            q_list = data.getlist("quantities")
            for i in range(len(i_list)):
                try:
                    q = int(q_list[i])
                    d.ingredients.add(i_list[i], through_defaults={'quantity': q})
                except ValueError:
                    pass

            d.save()

            if Dish.objects.filter(accepted=False).count() > 0:
                send_mail(
                    'Niezaakceptowane przepisy',
                    'Here is the message.',
                    'django@django.com',
                    ['karkru4@gmail.com'],
                    fail_silently=False,
                )
        return redirect('/recipe')
    raise Http404


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_recipe_to_default(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        form = RecipeForm()
        return render(request, "food/new_recipe_form.html", {"ingredients": ingredients, 'form': form})
    elif request.method == 'POST':
        data = request.POST.copy()
        # needed only because of the ingredients not in form but in html
        form = RecipeForm(data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            d = form.save(commit=False)
            d.save()
            i_list = [Ingredient.objects.get(name=ing) for ing in data.getlist("ingredients")]
            q_list = data.getlist("quantities")
            for i in range(len(i_list)):
                try:
                    q = int(q_list[i])
                    d.ingredients.add(i_list[i], through_defaults={'quantity': q})
                except ValueError:
                    pass
            d.save()
            file_name = "default_db.json"
            with open(file_name, 'r', encoding='utf-8') as file:
                db = json.load(file)
                ingredients_data = []
                ingredient_names=data.getlist("ingredients")
                for i in range(len(i_list)):
                    ingredients_data.append({"name": ingredient_names[i],
                                             "quantity": int(q_list[i])})
                recipes_data = db['recipes']
                recipes_data.append({"name": form.cleaned_data["name"],
                                     "description": form.cleaned_data["description"],
                                     "recipe": form.cleaned_data['recipe'],
                                     "ingredients": ingredients_data})

            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(db, file)
        return redirect('/recipe')
    raise Http404

@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def accept_recipes(request):
    dishes = Dish.objects.filter(accepted=False)
    return render(request, "food/recipe.html", {"list_items": dishes})

def recipe_id(request, dish_id):
    dish = Dish.objects.filter(id=dish_id)
    if not dish:
        raise Http404
    return render(request, "food/recipe_id_get.html", {"item": dish.get(id=dish_id)})


@login_required(login_url='/accounts/login')  # TODO: change to checking ownership
def recipe_id_delete(request, dish_id):
    dish = Dish.objects.filter(id=dish_id)
    if not dish:
        raise Http404
    dish.delete()
    return redirect('/recipe')

@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def recipe_id_accept(request, dish_id):
    dish = Dish.objects.filter(id=dish_id).update(accepted=True)
    if not dish:
        raise Http404
    return redirect('/recipe/accept')
