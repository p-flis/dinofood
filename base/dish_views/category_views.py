from django.shortcuts import render, redirect
from django.http import Http404

from base.models import *


def category(request):
    categories = Category.objects.all()
    return render(request, "food/category.html", {"list_items": categories})


def add_category(request):
    if request.method == 'GET':
        return render(request, "food/new_category_form.html")
    elif request.method == 'POST':
        data = request.POST.copy()
        # print(data)
        c = Category(name=data["name"])
        c.save()
        return redirect('/category')
    raise Http404


def category_id(request, cat_id):
    cat = Category.objects.filter(id=cat_id)
    if not cat:
        raise Http404
    return render(request, "food/category_id_get.html", {"item": cat.get(id=cat_id)})


def category_id_delete(request, cat_id):
    cat = Category.objects.filter(id=cat_id)
    if not cat:
        raise Http404
    cat.delete()
    return redirect('/category')
