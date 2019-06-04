from django import forms
from .models import *


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "name",
            'price',
            'units',
            'is_vegetarian',
            'is_vegan',
            'is_gluten_free',
        ]


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            "name",
            'description',
            'recipe',
            'image',
            'tools'
        ]


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            "name",
            'amount'
        ]


class CookingToolForm(forms.ModelForm):
    class Meta:
        model = CookingTool
        fields = [
            "name"
        ]
