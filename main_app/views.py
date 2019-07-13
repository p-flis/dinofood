from django.shortcuts import render
from main_app.forms import *
from django.forms.formsets import formset_factory
import django.views.generic as generic


class Index(generic.TemplateView):
    template_name = "home.html"


def display_form_errors(form):
    print('Invalid form')
    print('reasons: ')
    for reason in form.errors:
        print(reason)
        for error in form.errors[reason]:
            print(error)


def test_view(request):
    print('TEST')
    ingredient_form_set = formset_factory(IngredientOptionForm, extra=2, min_num=1, validate_min=True)
    if request.method == 'POST':
        formset = ingredient_form_set(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = ingredient_form_set()

    return render(request, 'test.html', {'formset': formset})


class SearchUnits(generic.TemplateView):
    template_name = 'ajax_search.html'
    http_method_names = ['get', 'post']

    def prepare_units(self, search_text, form_id):
        unit_id = '#' + form_id[:form_id.rfind('-') + 1] + 'unit'
        ing = Ingredient.objects.filter(id=search_text).get()
        self.extra_context = {"units": ing.units.all(), "unit_id": unit_id}

    def post(self, request, *args, **kwargs):
        search_text = request.POST['search_text']
        form_id = request.POST['form_id']
        self.prepare_units(search_text, form_id)
        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.prepare_units("", "")
        return super().get(request, *args, **kwargs)

