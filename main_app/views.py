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
    IngredientFormSet = formset_factory(Magic, extra=2)
    if request.method == 'POST':
        formset = IngredientFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = IngredientFormSet()

    return render(request, 'test.html', {'formset': formset})

