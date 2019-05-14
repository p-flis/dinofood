from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from base.forms import CategoryForm
from base.models import *


def category(request):
    categories = Category.objects.all()
    return render(request, "food/category.html", {"list_items": categories})

@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_category(request):
    if request.method == 'GET':
        form = CategoryForm()
        args = {"form":form}
        return render(request, "food/new_category_form.html", args)
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            c = Category(name=form.cleaned_data["name"])
            c.save()
        return redirect('/category')
    raise Http404

def category_id(request, cat_id):
    cat = Category.objects.filter(id=cat_id)
    if not cat:
        raise Http404
    return render(request, "food/category_id_get.html", {"item": cat.get(id=cat_id)})

@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def category_id_delete(request, cat_id):
    cat = Category.objects.filter(id=cat_id)
    if not cat:
        raise Http404
    cat.delete()
    return redirect('/category')

@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def category_id_update(request, cat_id):
    if request.method == 'GET':
        cat = Category.objects.filter(id=cat_id)
        if not cat:
            raise Http404
        item = cat.get(id=cat_id)
        data = {'name': item.name}
        form = CategoryForm(data)
        args =  {"form":form}
        return render(request, "food/new_category_form.html",args)
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = Category.objects.filter(id=cat_id)
            if cat:
                cat.update(name = form.cleaned_data["name"])
            else:
                c = Category(name=form.cleaned_data["name"])
                c.save()
        return redirect('/category')
    return redirect('/category')
