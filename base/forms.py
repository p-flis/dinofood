from django import forms
from base.models import Category

class IngredientForm(forms.Form):
    name = forms.CharField()
    price = forms.DecimalField(min_value=0, max_digits=8, decimal_places=2)
    category = forms.ChoiceField(choices=[(x.name, x.name) for x in Category.objects.all()])
    #choiceField needs list of 2-tuples, as one value is presented to the user,
    #and second one is the corresponding real one. We are currently using the
    #name of the category as an index, so x.name presented is x.name beneath

class CategoryForm(forms.Form):
    name = forms.CharField()

class RecipeForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    recipe = forms.CharField(required=False)
