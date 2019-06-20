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


class Magic(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ingredients = [(ing.id, ing.name) for ing in Ingredient.objects.all()]
        self.units = [(ing.id, ing.name) for ing in Unit.objects.all()]
        self.ingredient = forms.CharField(
            label='Ingredient',
            widget=forms.Select(choices=self.ingredients))
        self.quantity = forms.FloatField()
        self.unit = forms.CharField(
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

    ingredients = forms.MultipleChoiceField(choices={},
                                            widget=widgets.CheckboxSelectMultiple,
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
