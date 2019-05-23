from django.test import TestCase
from django.urls import reverse

from main_app.models import *


class RecipeSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ingredient_data = [
            ("Water", 2, "Liquids"),
            ("Lemon", 8, "Fruits"),
            ("Apple", 5, "Fruits")
        ]
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1]) for n in ingredient_data])
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
            ("Apple juice",
             "water, but tastes like apple",
             ["Water", "Apple"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    def test_view_url_exists_at_desired_location_id_exists(self):
        response = self.client.get('/recipe/search')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_get(self):
        response = self.client.get('/recipe/search')
        self.assertTemplateUsed(response, 'food/search_recipe.html')

    def test_view_uses_correct_template_post(self):
        ingredients_list = ['Water']
        response = self.client.post('/recipe/search',
                                    {"ingredients_in_fridge": ingredients_list,
                                     "ingredients_in_recipe": ingredients_list,
                                     "extra_money": 0})
        self.assertTemplateUsed(response, 'food/recipe.html')

    def test_view_finds_single_dish_from_fridge(self):
        ingredients_list = ['Water', 'Lemon']
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": ingredients_list,
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 0})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Lemonade')

    def test_view_finds_two_dishes_from_fridge(self):
        ingredients_list = ['Water', 'Lemon', 'Apple']
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": ingredients_list,
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 0})
        self.assertEqual(response.context['list_items'].count(), 2)

    def test_view_finds_single_dish_from_recipe(self):
        ingredients_list = ['Water', 'Lemon']
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": ingredients_list,
                                                       "extra_money": 999})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Lemonade')

    def test_view_finds_two_dishes_from_recipe(self):
        ingredients_list = ['Water']
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": ingredients_list,
                                                       "extra_money": 999})
        self.assertEqual(response.context['list_items'].count(), 2)

    def test_view_finds_single_dish_from_money(self):
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 7})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Apple juice')

    def test_view_finds_two_dishes_from_money(self):
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 10})
        self.assertEqual(response.context['list_items'].count(), 2)

    def test_view_finds_no_dishes(self):
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": [],
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 0})
        self.assertEqual(response.context['list_items'].count(), 0)

    def test_view_finds_single_dish_mix_fridge_money(self):
        ingredients_list = ['Water']
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": ingredients_list,
                                                       "ingredients_in_recipe": [],
                                                       "extra_money": 5})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Apple juice')

    def test_view_finds_single_dish_mix_fridge_recipe(self):
        fridge_ingredients_list = ['Water', 'Lemon', 'Apple']
        recipe_ingredients_list = ['Lemon']
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": fridge_ingredients_list,
                                                       "ingredients_in_recipe": recipe_ingredients_list,
                                                       "extra_money": 0})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Lemonade')

    def test_view_finds_single_dish_mix_fridge_recipe_money(self):
        fridge_ingredients_list = ['Water']
        recipe_ingredients_list = ['Lemon']
        response = self.client.post('/recipe/search', {"ingredients_in_fridge": fridge_ingredients_list,
                                                       "ingredients_in_recipe": recipe_ingredients_list,
                                                       "extra_money": 8})
        self.assertEqual(response.context['list_items'].count(), 1)
        self.assertEqual(response.context['list_items'][0].name, 'Lemonade')
