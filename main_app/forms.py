from django import forms
from .models import *
from accounts.models import User
from django.forms import widgets
import json


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


class IngredientOptionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ingredients = [(ing.id, ing.name) for ing in Ingredient.objects.all()]
        if(len(self.ingredients)==0):
            self.units = []
        else:
            self.units = [(unit.id, unit.name) for unit in Ingredient.objects.get(id=self.ingredients[0][0]).units.all()]

        self.fields['ingredient'] = forms.CharField(
            label='Ingredient',
            widget=forms.Select(choices=self.ingredients, attrs={"onchange": "happyFunction(event, this);"}))
        self.fields['quantity'] = forms.FloatField()
        self.fields['unit'] = forms.CharField(
            label='Unit',
            widget=forms.Select(choices=self.units))


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
        widgets = {
            "ingredients": widgets.CheckboxSelectMultiple
        }


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
    # TODO: extra_money should be optional for a user
    # I mean like checkbox "I'm poor"
    extra_money = forms.DecimalField(initial=999)
    is_vegetarian = forms.BooleanField(required=False)
    is_vegan = forms.BooleanField(required=False)
    is_gluten_free = forms.BooleanField(required=False)
    is_favourite = forms.BooleanField(required=False)


class IngredientsCheckboxesWidget(widgets.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        self.template_name = 'form/ingredientscheckboxes_widget.html'
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ctx.update(dict(approximate_costs=self.approximate_costs))
        return ctx

    class Media:
        js = ('js/jquery-3.4.1.min.js', 'js/checkboxespricedisplayer.js',)


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
        self.fields['ingredients'].widget.approximate_costs = json.dumps( \
            {
                obj.ingredient.id: int(obj.quantity * obj.unit.amount * obj.ingredient.price * 100) \
                for obj in self.recipe.recipeingredient_set.all()
            })

    ingredients = forms.MultipleChoiceField(choices={},
                                            widget=IngredientsCheckboxesWidget,
                                            required=False
                                            )


class DatalistWidget(forms.HiddenInput):
    template_name = 'form/datalist_widget.html'

    def __init__(self, datalist, name, *args, **kwargs):
        super(DatalistWidget, self).__init__(*args, **kwargs)
        self.attrs['list'] = datalist
        self.attrs['list_name'] = name


class DatalistInputWidget(forms.TextInput):
    def __init__(self, name, *args, **kwargs):
        super(DatalistInputWidget, self).__init__(*args, **kwargs)
        self.attrs.update({'list': f'{name}__list'})


class RecipeIngredientWidget(widgets.MultiWidget):
    def __init__(self, name, attrs=None):
        _widgets = (
            DatalistInputWidget(name=name, attrs=attrs),
            widgets.NumberInput(attrs=attrs),
            widgets.Select(attrs=attrs, choices=[(uni.id, uni.name) for uni in Unit.objects.all()])
        )
        super(RecipeIngredientWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            # return [value.quantity, value.unit.id]
            return [value.ingredient.name, value.quantity, value.unit.id]
        return [None, None, None]


class RecipeIngredientField(forms.MultiValueField):
    widget = RecipeIngredientWidget

    def __init__(self, name, *args, **kwargs):
        self.widget = RecipeIngredientWidget(name=name)
        fields = (
            forms.CharField(),
            forms.DecimalField(),
            forms.ChoiceField()
        )
        super(RecipeIngredientField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return " ".join(data_list)


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

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        # self.fields["recipe_ing"] = RecipeIngredientField(name="ings", required=False)
        # - to jest pole odpowiadające jednemu recipeingredient
        # todo Paweł zrób żeby działało
        #  pamietaj, żeby zmienić w new_recipe_form bo tam są wyświetlane poszczególne pola, to nie
        # self.fields["recipe_list"] = forms.Field(
        #     widget=DatalistWidget(datalist=[ing.name for ing in Ingredient.objects.all()], name="ings"),
        #     required=False
        # )
        # todo to pole wystarczy załączyć raz - ono doda datalist, a wszystkie inputy mogą (powinny) korzystać z jednego
