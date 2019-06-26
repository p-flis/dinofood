from django.shortcuts import render
from main_app.forms import *
from django.forms.formsets import formset_factory


# Create your views here.
def index(request):
    # return HttpResponse('base Karol!')
    return render(request, "home.html")


def displayFormErrors(form):
    print('Invalid form')
    print('reasons: ')
    for reason in form.errors:
        print(reason)
        for error in form.errors[reason]:
            print(error)


def test_view(request):
    print('TEST')
    IngredientFormSet = formset_factory(Magic, extra=2, min_num=1, validate_min=True)
    if request.method == 'POST':
        formset = IngredientFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = IngredientFormSet()

    return render(request, 'test.html', {'formset': formset})


def search_units(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
        form_id = request.POST['form_id']
    else:
        search_text = ""
        form_id = ""
    unit_id = '#' + form_id[:form_id.rfind('-') + 1] + 'unit'
    ing = Ingredient.objects.filter(id=search_text).get()
    return render(request, 'ajax_search.html', {"units": ing.units.all(), "unit_id": unit_id})
