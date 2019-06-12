from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *
from django.test import tag

from main_app.tests.TestSetupDatabase import *
from main_app.forms import *


# https://test-driven-django-development.readthedocs.io/en/latest/05-forms.html

@tag('form')
class IngredientFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(ingredients=True, tools=True, units=True, recipes=True)

    def test_init(self):
        IngredientForm()

    def test_init_with_instance(self):
        IngredientForm(instance=Ingredient.objects.first())

    def test_valid_data(self):
        u = Unit.objects.first()
        f = IngredientForm({
            "name": "Burak",
            "price": 5,
            "units": [u],
            "is_vegetarian": False,
            "is_vegan": True,
            "is_gluten_free": False
        })
        self.assertTrue(f.is_valid())
        ingredient = f.save()
        self.assertEquals(ingredient.name, "Burak")
        self.assertEquals(ingredient.price, 5)
        self.assertEquals(len([ingredient.units.all()]), 1)
        self.assertEquals(ingredient.units.first().name, u.name)
        self.assertEquals(ingredient.is_vegetarian, False)
        self.assertEquals(ingredient.is_vegan, True)
        self.assertEquals(ingredient.is_gluten_free, False)

    def test_blank_data(self):
        form = IngredientForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'price': ['This field is required.']
        })

    def test_update_data(self):
        f = IngredientForm(instance=Ingredient.objects.get(name="Woda"))
        self.assertEquals(f.initial["name"],"Woda")
        self.assertEquals(f.initial["price"], 2)
        self.assertEquals(f.initial["units"], [u for u in Ingredient.objects.get(name="Woda").units.all()])
        self.assertEquals(f.initial["is_vegetarian"], False)
        self.assertEquals(f.initial["is_vegan"], False)
        self.assertEquals(f.initial["is_gluten_free"], True)