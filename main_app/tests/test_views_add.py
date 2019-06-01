from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *

from main_app.tests.TestSetupDatabase import *


class AddRecipeViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipe/new')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/new_recipe_form.html')

    def test_view_adds_recipe(self):
        ingredient_data = [
            ("Water", 2, True, True, True),
            ("Lemon", 8, True, True, True),

        ]
        TestDatabase.create_custom_test_database(ingredient_data=ingredient_data)

        ingredients_list = ['Water', 'Lemon']
        quantities_list = ['1', '1']
        response = self.client.post('/recipe/new', {'name': 'Lemonade',
                                                    'description': 'water, but sour',
                                                    'recipe': 'hahaha to jest wymagane',
                                                    'ingredients': ingredients_list,
                                                    'quantities': quantities_list,
                                                    'image': ''})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())
        self.assertEqual(response.url, '/recipe')

    def test_view_adds_recipe_redirect(self):
        ingredient_data = [
            ("Water", 2, True, True, True),
            ("Lemon", 8, True, True, True),

        ]
        TestDatabase.create_custom_test_database(ingredient_data=ingredient_data)

        ingredients_list = ['Water', 'Lemon']
        quantities_list = ['1', '1']
        response = self.client.post('/recipe/new',
                                    {'name': 'Lemonade',
                                     'description': 'water, but sour',
                                     'recipe': 'hahaha to jest wymagane',
                                     'ingredients': ingredients_list,
                                     'quantities': quantities_list},
                                    follow=True)
        self.assertRedirects(response, reverse('recipe'), status_code=302, target_status_code=200)


class AddRecipeViewTestNotLoggedUser(TestCase):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('add_recipe'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('add_recipe'), status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        ingredients_list = ['Water', 'Lemon']
        quantities_list = ['1', '1']
        response = self.client.post('/recipe/new',
                                    {'name': 'Lemonade',
                                     'description': 'water, but sour',
                                     'recipe': 'hahaha to jest wymagane',
                                     'ingredients': ingredients_list,
                                     'quantities': quantities_list},
                                    follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('add_recipe'), status_code=302,
                             target_status_code=200)
        self.assertFalse(Dish.objects.filter(name='Lemonade').exists())


class AddIngredientViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ingredient/new')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add_ingredient'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_ingredient'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/new_ingredient_form.html')

    def test_view_adds_ingredient(self):
        response = self.client.post('/ingredient/new', {'name': 'water', 'price': '2', 'is_vegetarian':'false', 'is_vegan':'false', 'is_gluten_free':'false'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name='water').exists())
        self.assertEqual(response.url, '/ingredient')

    def test_view_adds_ingredient_redirect(self):
        response = self.client.post('/ingredient/new', {'name': 'water', 'price': '2', 'is_vegetarian':'false', 'is_vegan':'false', 'is_gluten_free':'false'}, follow=True)
        self.assertRedirects(response,
                             reverse('ingredient'),
                             status_code=302,
                             target_status_code=200)


class AddIngredientViewTestNotSuperuser(TestCase):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('add_ingredient'), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_ingredient'),
                             status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        response = self.client.post('/ingredient/new', {'name': 'water', 'price': '2'}, follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_ingredient'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(Ingredient.objects.filter(name='water').exists())
