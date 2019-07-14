from main_app.models import *
import django.views.generic as generic
import main_app.custom_mixins as custom_mixins
from django.urls import reverse_lazy


class IngredientList(custom_mixins.SuperuserRequiredMixin, generic.ListView):
    model = Ingredient
    context_object_name = "list_items"


class AddIngredient(custom_mixins.SuperuserRequiredMixin, generic.CreateView):
    model = Ingredient
    success_url = reverse_lazy('ingredient')
    fields = '__all__'


class IngredientId(custom_mixins.SuperuserRequiredMixin, generic.DetailView):
    model = Ingredient
    pk_url_kwarg = 'object_id'
    context_object_name = "item"


class IngredientDelete(custom_mixins.SuperuserRequiredMixin, generic.DeleteView):
    model = Ingredient
    pk_url_kwarg = 'object_id'
    success_url = reverse_lazy('ingredient')


class IngredientUpdate(custom_mixins.SuperuserRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = '__all__'
    pk_url_kwarg = 'object_id'
    success_url = reverse_lazy('ingredient')
