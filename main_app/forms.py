from django import forms
from .models import *

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "name",
            'price',
        ]

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            "name",
            'description',
            'recipe',
            'image',
        ]
