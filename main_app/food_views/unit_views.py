from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from main_app.forms import UnitForm
from main_app.models import *
import json


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def unit(request):
    units = Unit.objects.all()
    return render(request, "food/units.html", {"list_items": units})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_unit(request):
    if request.method == 'GET':
        form = UnitForm()
        args = {"form": form}
        return render(request, "food/new_unit_form.html", args)
    elif request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/unit')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def unit_id(request, object_id):
    uni = Unit.objects.filter(id=object_id)
    if not uni:
        raise Http404
    return render(request, "food/unit_id_get.html", {"item": uni.get(id=object_id)})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def unit_id_delete(request, object_id):
    uni = Unit.objects.filter(id=object_id)
    if not uni:
        raise Http404
    uni = uni.get()
    uni.delete()
    return redirect('/unit')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def unit_id_update(request, object_id):
    if request.method == 'GET':
        uni = Unit.objects.filter(id=object_id)
        if not uni:
            raise Http404
        uni = uni.get()
        form = UnitForm(instance=uni)
        args = {"form": form}
        return render(request, "food/new_unit_form.html", args)
    elif request.method == 'POST':
        instance = Unit.objects.get(id=object_id)
        form = UnitForm(instance=instance, data=request.POST)
        # print("checkpoint1")
        if form.is_valid():
            form.save()
        return redirect('/unit')
