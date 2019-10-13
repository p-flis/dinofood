from django import forms
from .models import *
from accounts.models import User


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
        model = Recipe
        fields = [
            "name",
            'description',
            'recipe_text',
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


class FridgeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "ingredients"
        ]


class ToolsUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "tools"
        ]


class SearchForm(forms.Form):
    ingredients_in_fridge = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), required=False)
    tools_in_kitchen = forms.ModelMultipleChoiceField(queryset=CookingTool.objects.all(), required=False)
    ingredients_in_recipe = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), required=False)
    extra_money = forms.DecimalField(initial=999)
    is_vegetarian = forms.BooleanField(required=False)
    is_vegan = forms.BooleanField(required=False)
    is_gluten_free = forms.BooleanField(required=False)
    is_favourite = forms.BooleanField(required=False)
