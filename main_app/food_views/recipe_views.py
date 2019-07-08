from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, JsonResponse
from django.conf import settings
from main_app.forms import RecipeForm, RecipeIdIngredientsForm
from main_app.models import *
from accounts.models import *
from main_app.forms import *
from django.forms.formsets import formset_factory
from main_app.views import displayFormErrors
from django.core.mail import send_mail
from django.contrib import messages
import json



def recipe(request):
    recipes = Recipe.objects.filter(accepted=True)
    return render(request, "food/recipe.html", {"list_items": recipes})


@login_required(login_url='/accounts/login')
def add_recipe(request):
    IngredientFormSet = formset_factory(IngredientOptionForm, extra=2, min_num=1, validate_min=True)
    if request.method == 'GET':
        formset = IngredientFormSet()
        ingredients = Ingredient.objects.all().order_by('name')
        # form = RecipeForm(initial={'recipe_ing':RecipeIngredient.objects.first()})
        # todo Paweł, jak to odkomentujesz to tam do tego pola doda pierwszy (losowy) recipeingredient,
        #  to tylko żeby sprawdzić widget
        form = RecipeForm()
        return render(request, "food/new_recipe_form.html", {"ingredients": ingredients, 'form': form, 'formset': formset})
    elif request.method == 'POST':
        formset = IngredientFormSet(request.POST, request.FILES)
        i_list = []
        q_list = []
        u_list = []
        if formset.is_valid():
            for f in formset:
                cd = f.cleaned_data
                i_list.append(Ingredient.objects.get(id=cd.get('ingredient')))
                q_list.append(cd.get('quantity'))
                u_list.append(Unit.objects.get(id=cd.get('unit')))
        # needed only because of the ingredients not in form but in html
        form = RecipeForm(data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            recipe_model = form.save(commit=False)
            recipe_model.save()
            for i in range(len(i_list)):
                try:
                    q = int(q_list[i])
                    u = u_list[i]
                    recipe_model.ingredients.add(i_list[i], through_defaults={'quantity': q, 'unit': u})
                except ValueError:
                    print("what:")
                    pass
            recipe_model.owner = User.objects.get(username=request.user.username)
            recipe_model.accepted = request.user.is_superuser
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
def accept_recipes(request):
    recipes = Recipe.objects.filter(accepted=False)
    return render(request, "food/recipe.html", {"list_items": recipes})


def recipe_id(request, object_id):
    recipe_model = Recipe.objects.filter(id=object_id)
    if request.user.is_authenticated:
        rating = Rating.objects.filter(recipe=recipe_model.first(), user=request.user)
    else:
        rating = None
    if not recipe_model:
        raise Http404
    recipe_model = recipe_model.first()
    form = RecipeIdIngredientsForm(recipe=recipe_model)
    if request.user.is_authenticated:
        form.initial = {"ingredients": [ing.id for ing in request.user.ingredients.all()]}
    return render(request, "food/recipe_id_get.html", {"item": recipe_model,
                                                       "rating": rating,
                                                       "form": form,})


def recipe_id_rate(request, object_id):
    if request.method == 'GET':
        recipe = Recipe.objects.get(id=object_id)
        mean = recipe.average_rating()
        if request.user.is_authenticated:
            user = request.user
            prev_rating = Rating.objects.filter(user=user, recipe=recipe)
            if len(prev_rating) > 0:
                output_data = {'rating': prev_rating[0].rating, 'mean': mean, 'favourite': prev_rating[0].favourite}
            else:
                output_data = {'rating': None, 'mean': mean, 'favourite': False}
        else:
            output_data = {'rating': None, 'mean': mean, 'favourite': False}
        return JsonResponse(output_data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            # messages.error(request, "") TODO:change to reporting an error for stardisplayer to understand
            return JsonResponse({'rating': None, 'mean': None, 'favourite':None})
        data = request.POST.copy()
        if data is None:
            return JsonResponse({'rating': None, 'mean': None, 'favourite':None})
        rating = data.get("rating")
        favourite = data.get("favourite")
        if favourite is None \
                or (favourite is False and rating is None) \
                or rating not in [None,'1','2','3','4','5']:
            return JsonResponse({'rating': None, 'mean': None, 'favourite':None})
        user = request.user
        recipe = Recipe.objects.get(id=object_id)
        prev_rating = Rating.objects.filter(user=user, recipe=recipe)
        if (rating == None):  # the heart has been clicked, we edit only favourite
            if len(prev_rating) > 0:
                prev_rating = prev_rating[0]
                prev_rating.favourite = (data.get("favourite") == 'true');
                prev_rating.save()
                new_rating = prev_rating
            else:
                new_rating = Rating(user=user, recipe=recipe, rating=None, favourite=True)
        else:
            rating = int(rating)
            if len(prev_rating) > 0:
                prev_rating = prev_rating[0]
                if prev_rating.rating is None:
                    recipe.times_rated = recipe.times_rated + 1
                    recipe.sum_rating = recipe.sum_rating + rating
                else:
                    recipe.sum_rating = recipe.sum_rating - prev_rating.rating + rating
                prev_rating.rating = rating
                new_rating = prev_rating
            else:
                new_rating = Rating(user=user, recipe=recipe, rating=rating, favourite=False)
                recipe.sum_rating = recipe.sum_rating + rating
                recipe.times_rated = recipe.times_rated + 1

        new_rating.save()
        recipe.save()
        mean = recipe.average_rating()
        output_data = {'rating': new_rating.rating, 'mean': mean, 'favourite': new_rating.favourite}
        return JsonResponse(output_data)
    return redirect('/recipe')


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
