from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from main_app.forms import CookingToolForm
from main_app.models import *
import json


def cooking_tool(request):
    cooking_tools = CookingTool.objects.all()
    return render(request, "food/cooking_tools.html", {"list_items": cooking_tools})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_cooking_tool(request):
    if request.method == 'GET':
        form = CookingToolForm()
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        form = CookingToolForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/cooking_tool')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_cooking_tool_to_default(request):
    if request.method == 'GET':
        form = CookingToolForm()
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        form = CookingToolForm(request.POST)
        if form.is_valid():
            form.save()
            file_name = "default_db.json"
            with open(file_name, 'r', encoding='utf-8') as file:
                db = json.load(file)
                cooking_tools_data = db['cooking_tools']
                cooking_tools_data.append({"name": form.cleaned_data["name"]})
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(db, file)
        return redirect('/cooking_tool')


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
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        instance = CookingTool.objects.get(id=object_id)
        form = CookingToolForm(instance=instance, data=request.POST)
        # print("checkpoint1")
        if form.is_valid():
            form.save()
        return redirect('/cooking_tool')
