from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.conf import settings
from main_app.forms import RecipeForm
from main_app.models import *
from accounts.models import *
from main_app.views import displayFormErrors
from django.core.mail import send_mail
import json


def recipe(request):
    recipes = Recipe.objects.all()
    return render(request, "food/recipe.html", {"list_items": recipes})


@login_required(login_url='/accounts/login')
def add_recipe(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all().order_by('name')
        form = RecipeForm()
        return render(request, "food/new_recipe_form.html", {"ingredients": ingredients, 'form': form})
    elif request.method == 'POST':

        data = request.POST.copy()
        # needed only because of the ingredients not in form but in html
        form = RecipeForm(data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            recipe_model = form.save(commit=False)
            recipe_model.save()
            i_list = [Ingredient.objects.get(name=ing) for ing in data.getlist("ingredients")]
            q_list = data.getlist("quantities")
            for i in range(len(i_list)):
                try:
                    q = int(q_list[i])
                    recipe_model.ingredients.add(i_list[i], through_defaults={'quantity': q})
                except ValueError:
                    pass
            recipe_model.owner = User.objects.get(username=request.user.username)
            if request.user.is_superuser:
                recipe_model.accepted = True
            recipe_model.save()
            recipe_model.save()

            if Recipe.objects.filter(accepted=False).count() == 1:
                send_mail(
                    'Unaccepted recipes',
                    'Sth happened.',
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
        else:
            displayFormErrors(form)
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
            recipe_model = form.save(commit=False)
            recipe_model.save()
            i_list = [Ingredient.objects.get(name=ing) for ing in data.getlist("ingredients")]
            q_list = data.getlist("quantities")
            for i in range(len(i_list)):
                try:
                    q = int(q_list[i])
                    recipe_model.ingredients.add(i_list[i], through_defaults={'quantity': q})
                except ValueError:
                    pass
            recipe_model.save()
            file_name = "default_db.json"
            with open(file_name, 'r', encoding='utf-8') as file:
                db = json.load(file)
                ingredients_data = []
                ingredient_names = data.getlist("ingredients")
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
    recipes = Recipe.objects.filter(accepted=False)
    return render(request, "food/recipe.html", {"list_items": recipes})


def recipe_id(request, object_id):
    recipe_model = Recipe.objects.filter(id=object_id)
    if request.user.is_authenticated:
        rating = Rating.objects.filter(recipe=recipe_model[0], user=request.user)
    else:
        rating=None
    if not recipe_model:
        raise Http404
    return render(request, "food/recipe_id_get.html", {"item": recipe_model.get(id=object_id), "rating": rating})


@login_required(login_url='/accounts/login')
def recipe_id_delete(request, object_id):
    recipe_model = Recipe.objects.filter(id=object_id)
    if not recipe_model:
        raise Http404
    if recipe_model.get().owner != request.user and not request.user.is_superuser:
        # I'm pretty sure this is not very secure
        return redirect('/accounts/login/?next=' + request.path)
    recipe_model.delete()
    return redirect('/recipe')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def recipe_id_accept(request, object_id):
    recipe_model = Recipe.objects.filter(id=object_id).update(accepted=True)
    if not recipe_model:
        raise Http404
    return redirect('/recipe/accept')
