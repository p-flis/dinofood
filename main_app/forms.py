from django import forms
from .models import *
from accounts.models import User
from django.forms import widgets


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


# chyba coś takiego
# class RecipeIngredientWidget(widgets.MultiWidget):
#     def __init__(self, ingredients, units, attrs=None):
#         ingredients = [(ing.id,ing.name) for ing in ingredients]
#         units = [(ing.id,ing.name) for ing in units]
#         _widgets = (
#             widgets.SelectMultiple(attrs=attrs, choices=ingredients),
#             widgets.NumberInput(attrs=attrs),
#             widgets.Select(attrs=attrs, choices=units),
#         )
#         super().__init__(_widgets, attrs)
#
#     def decompress(self, value):
#         if value:
#             return [value.ingredient.id, value.quantity, value.unit.id]
#         return [None,None,None]

class Magic(forms.Form):
    ingredients = [(ing.id, ing.name) for ing in Ingredient.objects.all()]
    units = [(ing.id, ing.name) for ing in Unit.objects.all()]
    ingredient = forms.CharField(
        label='Ingredient',
        widget=forms.Select(choices=ingredients))
    quantity = forms.FloatField()
    unit = forms.CharField(
        label='Unit',
        widget=forms.Select(choices=units))


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


class RecipeIdIngredientsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.recipe = kwargs.pop('recipe')
        super().__init__(*args, **kwargs)
        self.fields['ingredients'].queryset = self.recipe.recipeingredient_set
        self.fields['ingredients'].choices = \
            [
                (
                    obj.ingredient.id,
                    '{0}, {1}, {2} ({3} g)'.format(obj.ingredient.name, obj.quantity, obj.unit.name, obj.unit.amount)
                )
                for obj in self.recipe.recipeingredient_set.all()
            ]
        # def custom_label(obj):
        #     return '{0}, {1}, {2} ({3} g)'.format(obj.ingredient.name, obj.quantity, obj.unit.name, obj.unit.amount)
        #
        # self.fields['ingredients'].label_from_instance = custom_label

    ingredients = forms.MultipleChoiceField(choices={},
                                            widget=widgets.CheckboxSelectMultiple,
                                            required=False
                                            )
