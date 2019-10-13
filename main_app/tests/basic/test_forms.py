from main_app.tests.TestCaseSpecialUser import *
from django.test import tag
from main_app.forms import *
from main_app.tests.TestSetupDatabase import *

@tag('ingredient', 'form')
class IngredientFormTest(TestCase):
    def setUp(self):
        super().setUp();
        TestDatabase.create_default_test_database(units=True)

    def test_form_valid(self):
        gram = Unit.objects.get(name="Gram")
        form = IngredientForm(data={\
        'name': "rzodkiewka testowa", 'price': 100, 'units': [gram], 'is_vegan': True,\
        'is_vegetarian': True, 'is_gluten_free': True\
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_empty(self):
        gram = Unit.objects.get(name="Gram")
        form = IngredientForm()
        self.assertFalse(form.is_valid())

    def test_form_valid_no_units(self):
        gram = Unit.objects.get(name="Gram")
        form = IngredientForm(data={\
        'name': "rzodkiewka testowa", 'price': 100, 'is_vegan': True,\
        'is_vegetarian': True, 'is_gluten_free': True\
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_no_price(self):
        gram = Unit.objects.get(name="Gram")
        form = IngredientForm(data={\
        'name': "rzodkiewka testowa", 'units': [gram], 'is_vegan': True,\
        'is_vegetarian': True, 'is_gluten_free': True\
        })
        self.assertFalse(form.is_valid())

@tag('unit', 'form')
class UnitFormTest(TestCase):
    def test_form_valid(self):
        form = UnitForm(data={\
        'name': "uncja", 'amount': 28.35\
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_wrong_format(self):
        form = UnitForm(data={\
        'name': "masa Jowisza", 'amount': 1808000000000000000000000000000\
        })
        self.assertFalse(form.is_valid())

    def test_form_invalid_no_amount(self):
        form = UnitForm(data={\
        'name': "uncja"\
        })
        self.assertFalse(form.is_valid())

@tag('cooking_tool', 'form', 'CookingTool')
class CookingToolFormTest(TestCase):
    def test_form_valid(self):
        form = CookingToolForm(data={\
        'name': "klucz 15"
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_empty(self):
        form = CookingToolForm()
        self.assertFalse(form.is_valid())
