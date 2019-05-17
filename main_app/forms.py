from django import forms
from .models import *

class IngredientForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField()
        self.fields['price'] = forms.DecimalField(min_value=0, max_digits=8, decimal_places=2)
        self.fields['category'] = forms.ChoiceField(choices=[(x.name, x.name) for x in Category.objects.all()])
    # choiceField needs list of 2-tuples, as one value is presented to the user,
    # and second one is the corresponding real one. We are currently using the
    # name of the category as an index, so x.name presented is x.name beneath


class CategoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField()


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            "name",
            'description',
            'recipe',
            'image',
        ]
