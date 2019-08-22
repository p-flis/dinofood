from main_app.models import *
import django.views.generic as generic
import main_app.custom_mixins as custom_mixins
from django.urls import reverse_lazy


class CookingToolList(custom_mixins.SuperuserRequiredMixin, generic.ListView):
    model = CookingTool
    context_object_name = "list_items"


class AddCookingTool(custom_mixins.SuperuserRequiredMixin, generic.CreateView):
    model = CookingTool
    success_url = reverse_lazy('cooking_tool')
    fields = '__all__'


class CookingToolId(custom_mixins.SuperuserRequiredMixin, generic.DetailView):
    model = CookingTool
    pk_url_kwarg = 'object_id'
    context_object_name = "item"


class CookingToolDelete(custom_mixins.SuperuserRequiredMixin, generic.DeleteView):
    model = CookingTool
    pk_url_kwarg = 'object_id'
    success_url = reverse_lazy('cooking_tool')


class CookingToolUpdate(custom_mixins.SuperuserRequiredMixin, generic.UpdateView):
    model = CookingTool
    fields = '__all__'
    pk_url_kwarg = 'object_id'
    success_url = reverse_lazy('cooking_tool')
