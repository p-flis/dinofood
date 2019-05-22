from django import forms
from .models import *


class IngredientForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField()
        self.fields['price'] = forms.DecimalField(min_value=0, max_digits=8, decimal_places=2)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            "name",
            'description',
            'recipe',
            'image',
        ]
