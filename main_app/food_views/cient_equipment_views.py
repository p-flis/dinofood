from main_app.forms import FridgeUserForm, ToolsUserForm
import django.views.generic as generic
import django.contrib.auth.mixins as mixins
from django.urls import reverse_lazy


class ModifyFridge(mixins.LoginRequiredMixin, generic.UpdateView):
    success_url = reverse_lazy('recipe')
    template_name = 'client/fridge.html'
    form_class = FridgeUserForm

    def get_object(self, queryset=None):
        return self.request.user


class ModifyTools(mixins.LoginRequiredMixin, generic.UpdateView):
    success_url = reverse_lazy('recipe')
    template_name = 'client/tools.html'
    form_class = ToolsUserForm

    def get_object(self, queryset=None):
        return self.request.user

