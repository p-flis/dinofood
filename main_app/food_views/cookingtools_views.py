from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from main_app.forms import CookingToolForm
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


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def cooking_tool(request):
    cooking_tools = CookingTool.objects.all()
    return render(request, "food/cooking_tools.html", {"list_items": cooking_tools})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_cooking_tool(request):
    if request.method == 'GET':
        form = CookingToolForm()
        args = {"form": form}
        return render(request, "food/new_cooking_tool_form.html", args)
    elif request.method == 'POST':
        form = CookingToolForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/cooking_tool')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def cooking_tool_id(request, object_id):
    tool = CookingTool.objects.filter(id=object_id)
    if not tool:
        raise Http404
    return render(request, "food/cooking_tool_id_get.html", {"item": tool.get(id=object_id)})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def cooking_tool_id_delete(request, object_id):
    tool = CookingTool.objects.filter(id=object_id)
    if not tool:
        raise Http404
    tool = tool.get()
    tool.delete()
    return redirect('/cooking_tool')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def cooking_tool_id_update(request, object_id):
    if request.method == 'GET':
        tool = CookingTool.objects.filter(id=object_id)
        if not tool:
            raise Http404
        tool = tool.get()
        form = CookingToolForm(instance=tool)
        args = {"form": form}
        return render(request, "food/new_cooking_tool_form.html", args)
    elif request.method == 'POST':
        instance = CookingTool.objects.get(id=object_id)
        form = CookingToolForm(instance=instance, data=request.POST)
        # print("checkpoint1")
        if form.is_valid():
            form.save()
        return redirect('/cooking_tool')
