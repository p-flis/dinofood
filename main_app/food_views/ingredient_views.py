from main_app.models import *
<<<<<<< Updated upstream
from main_app.views import displayFormErrors
import json


def ingredient(request):
    ingredients = Ingredient.objects.all()
    return render(request, "food/ingredients.html", {"list_items": ingredients})
=======
import django.views.generic as generic
import main_app.custom_mixins as custom_mixins
from django.urls import reverse_lazy


class IngredientList(custom_mixins.SuperuserRequiredMixin, generic.ListView):
    model = Ingredient
    context_object_name = "list_items"
>>>>>>> Stashed changes


class AddIngredient(custom_mixins.SuperuserRequiredMixin, generic.CreateView):
    model = Ingredient
    success_url = reverse_lazy('ingredient')
    fields = '__all__'


<<<<<<< Updated upstream
def ingredient_id(request, object_id):
    ing = Ingredient.objects.filter(id=object_id)
    if not ing:
        raise Http404
    return render(request, "food/ingredient_id_get.html", {"item": ing.get(id=object_id)})
=======
class IngredientId(custom_mixins.SuperuserRequiredMixin, generic.DetailView):
    model = Ingredient
    pk_url_kwarg = 'object_id'
    context_object_name = "item"
>>>>>>> Stashed changes


class IngredientDelete(custom_mixins.SuperuserRequiredMixin, generic.DeleteView):
    model = Ingredient
    pk_url_kwarg = 'object_id'
    success_url = reverse_lazy('ingredient')


class IngredientUpdate(custom_mixins.SuperuserRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = '__all__'
    pk_url_kwarg = 'object_id'
    success_url = reverse_lazy('ingredient')
