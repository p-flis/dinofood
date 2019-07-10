from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from main_app.forms import IngredientForm
from main_app.models import *
import django.views.generic as generic
import main_app.custom_mixins as custom_mixins


class IngredientList(custom_mixins.SuperuserRequiredMixin, generic.ListView):
    model = Ingredient
    context_object_name = "list_items"
    template_name = "food/ingredients.html"


class AddIngredient(custom_mixins.SuperuserRequiredMixin, generic.CreateView):
    model = Ingredient
    template_name = "food/new_ingredient_form.html"
    success_url = '/ingredient'
    fields = '__all__'


class IngredientId(custom_mixins.SuperuserRequiredMixin, generic.DetailView):
    model = Ingredient
    pk_url_kwarg = 'object_id'
    context_object_name = "item"
    template_name = "food/ingredient_id_get.html"


class IngredientDelete(custom_mixins.SuperuserRequiredMixin, generic.DeleteView):
    model = Ingredient
    pk_url_kwarg = 'object_id'
    success_url = '/ingredient'
    template_name = 'food/ingredient_confirm_delete.html'


class IngredientUpdate(custom_mixins.SuperuserRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = '__all__'
    pk_url_kwarg = 'object_id'
    success_url = '/ingredient'
    template_name = 'food/new_ingredient_form.html'


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
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
        #     displayFormErrors(form)
        return redirect('/ingredient')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
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
        form = IngredientForm(instance=instance, data=request.POST)
        if form.is_valid():
            form.save()
        # else:
        #     displayFormErrors(form)

        return redirect('/ingredient')
