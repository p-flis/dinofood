from main_app.models import *
import django.views.generic as generic
import main_app.custom_mixins as custom_mixins
from django.urls import reverse_lazy


class UnitList(custom_mixins.SuperuserRequiredMixin, generic.ListView):
    model = Unit
    context_object_name = "list_items"


class AddUnit(custom_mixins.SuperuserRequiredMixin, generic.CreateView):
    model = Unit
    success_url = reverse_lazy('unit')
    fields = '__all__'


class UnitId(custom_mixins.SuperuserRequiredMixin, generic.DetailView):
    model = Unit
    pk_url_kwarg = 'object_id'
    context_object_name = "item"


class UnitDelete(custom_mixins.SuperuserRequiredMixin, generic.DeleteView):
    model = Unit
    pk_url_kwarg = 'object_id'
    success_url = reverse_lazy('unit')


class UnitUpdate(custom_mixins.SuperuserRequiredMixin, generic.UpdateView):
    model = Unit
    fields = '__all__'
    pk_url_kwarg = 'object_id'
    success_url = reverse_lazy('unit')
