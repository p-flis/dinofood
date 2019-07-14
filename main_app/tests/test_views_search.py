from django.test import TestCase
from django.urls import reverse
from main_app.tests.TestSetupDatabase import TestDatabase

from main_app.models import *


class RecipeSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(units=True, ingredients=True, tools=True, recipes=True)
        # ings: woda 2, cytryna 8, jabłko  5
        # lemoniada 1*Woda(gram)+2*Cytryna(kilo=10gram) = 2 + 2*8*10 = 162
        # sok jabłkowy 1*Woda(gram)+5*Jabłko(gram) = 2+5*5 = 27
        recipes_data = [
            {
                'name': "Sok jabłkowy",
                'description': "Woda, ale smakuje jak jabłko",
                'recipe': "Nie wiem",
                'ingredients': [
                    {
                        'name': "Woda",
                        'quantity': 1,
                        'unit': "Gram"
                    },
                    {
                        'name': "Jabłko",
                        'quantity': 5,
                        'unit': "Gram"
                    }
                ],
                'tools': [
                    {
                        'name': "Patelnia"
                    }
                ]
            }
        ]
        TestDatabase.append_custom_test_database(recipes_data=recipes_data)

    def test_view_url_exists_at_desired_location_id_exists(self):
        response = self.client.get(reverse('search_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_get(self):
        response = self.client.get(reverse('search_recipe'))
        self.assertTemplateUsed(response, 'main_app/recipe_search.html')

    def test_view_uses_correct_template_post(self):
        ingredients_list = Ingredient.objects.filter(name__in=["Woda"]).all()
        ingredients_list = [i.id for i in ingredients_list]
        response = self.client.post(reverse('search_recipe'),
                                    {"ingredients_in_fridge": ingredients_list,
                                     "ingredients_in_recipe": ingredients_list,
                                     "extra_money": 0,
                                     "is_vegetarian": False,
                                     "is_vegan": False,
                                     "is_gluten_free": False,
                                     "is_favourite": False})
        self.assertTemplateUsed(response, 'main_app/recipe_list.html')

    def test_view_finds_single_recipe_from_fridge(self):
        ingredients_list = Ingredient.objects.filter(name__in=['Woda', 'Cytryna']).all()
        ingredients_list = [i.id for i in ingredients_list]
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": ingredients_list,
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 0,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Lemoniada')

    def test_view_finds_two_recipes_from_fridge(self):
        ingredients_list = Ingredient.objects.filter(name__in=['Woda', 'Cytryna', 'Jabłko']).all()
        ingredients_list = [i.id for i in ingredients_list]
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": ingredients_list,
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 0,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 2)

    def test_view_finds_single_recipe_from_recipe(self):
        ingredients_list = Ingredient.objects.filter(name__in=['Woda', 'Cytryna']).all()
        ingredients_list = [i.id for i in ingredients_list]
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": ingredients_list,
                                                       "extra_money": 999,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Lemoniada')

    def test_view_finds_two_recipes_from_recipe(self):
        ingredients_list = Ingredient.objects.filter(name__in=['Woda']).all()
        ingredients_list = [i.id for i in ingredients_list]
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": ingredients_list,
                                                       "extra_money": 999,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 2)

    def test_view_finds_single_recipe_from_money(self):
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 30,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Sok jabłkowy')

    def test_view_finds_two_recipes_from_money(self):
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 500,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 2)

    def test_view_finds_no_recipes(self):
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 0,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 0)

    def test_view_finds_single_recipe_mix_fridge_money(self):
        ingredients_list = Ingredient.objects.filter(name__in=['Woda']).all()
        ingredients_list = [i.id for i in ingredients_list]
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": ingredients_list,
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 25,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Sok jabłkowy')

    def test_view_finds_single_recipe_mix_fridge_recipe(self):
        fridge_ingredients_list = Ingredient.objects.filter(name__in=['Woda', 'Cytryna', 'Jabłko']).all()
        fridge_ingredients_list = [i.id for i in fridge_ingredients_list]
        recipe_ingredients_list = Ingredient.objects.filter(name__in=['Cytryna']).all()
        recipe_ingredients_list = [i.id for i in recipe_ingredients_list]
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": fridge_ingredients_list,
                                                       "ingredients_in_recipe": recipe_ingredients_list,
                                                       "extra_money": 0,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Lemoniada')

    def test_view_finds_single_recipe_mix_fridge_recipe_money(self):
        fridge_ingredients_list = Ingredient.objects.filter(name__in=['Woda']).all()
        fridge_ingredients_list = [i.id for i in fridge_ingredients_list]
        recipe_ingredients_list = Ingredient.objects.filter(name__in=['Cytryna']).all()
        recipe_ingredients_list = [i.id for i in recipe_ingredients_list]
        response = self.client.post(reverse('search_recipe'), {"ingredients_in_fridge": fridge_ingredients_list,
                                                       "ingredients_in_recipe": recipe_ingredients_list,
                                                       "extra_money": 160,
                                                       "is_vegetarian": False,
                                                       "is_vegan": False,
                                                       "is_gluten_free": False,
                                                       "is_favourite": False})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Lemoniada')
