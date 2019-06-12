from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *
from django.test import tag

from main_app.tests.TestSetupDatabase import *


# region ingredients
@tag('client', 'fridge')
class ChangeFridgeTest(TestCaseLoggedUser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(ingredients=True, tools=True, units=True, recipes=True)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/fridge')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('fridge'))
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual('/fridge',reverse('fridge'))

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('fridge'))
        self.assertTemplateUsed(response, 'client/fridge.html')

