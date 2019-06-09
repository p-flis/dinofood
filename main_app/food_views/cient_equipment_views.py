from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from main_app.forms import FridgeUserForm, ToolsUserForm
from main_app.models import *
from main_app.views import displayFormErrors
import json


@login_required(login_url='/accounts/login')
def modify_fridge(request):
    if request.method == 'GET':
        usr = request.user
        form = FridgeUserForm(instance=usr)
        args = {"form": form}
        return render(request, "client/fridge.html", args)
    elif request.method == 'POST':
        usr = request.user
        form = FridgeUserForm(instance=usr, data=request.POST)
        if form.is_valid():
            form.save()
        # else:
        #     displayFormErrors(form)

        return redirect('/recipe')


@login_required(login_url='/accounts/login')
def modify_tools(request):
    if request.method == 'GET':
        usr = request.user
        form = ToolsUserForm(instance=usr)
        args = {"form": form}
        return render(request, "client/tools.html", args)
    elif request.method == 'POST':
        usr = request.user
        form = ToolsUserForm(instance=usr, data=request.POST)
        if form.is_valid():
            form.save()
        # else:
        #     displayFormErrors(form)

        return redirect('/recipe')
