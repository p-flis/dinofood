from main_app.models import *
import django.views.generic as generic
import main_app.custom_mixins as custom_mixins


class CookingToolList(custom_mixins.SuperuserRequiredMixin, generic.ListView):
    model = CookingTool
    context_object_name = "list_items"
    template_name = "food/cooking_tools.html"


class AddCookingTool(custom_mixins.SuperuserRequiredMixin, generic.CreateView):
    model = CookingTool
    template_name = "food/new_cooking_tool_form.html"
    success_url = '/cooking_tool'
    fields = '__all__'


class CookingToolId(custom_mixins.SuperuserRequiredMixin, generic.DetailView):
    model = CookingTool
    pk_url_kwarg = 'object_id'
    context_object_name = "item"
    template_name = "food/cooking_tool_id_get.html"


class CookingToolDelete(custom_mixins.SuperuserRequiredMixin, generic.DeleteView):
    model = CookingTool
    pk_url_kwarg = 'object_id'
    success_url = '/cooking_tool'
    template_name = 'food/cooking_tool_confirm_delete.html'


class CookingToolUpdate(custom_mixins.SuperuserRequiredMixin, generic.UpdateView):
    model = CookingTool
    fields = '__all__'
    pk_url_kwarg = 'object_id'
    success_url = '/cooking_tool'
    template_name = 'food/new_cooking_tool_form.html'
