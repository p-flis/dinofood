from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *
import django.contrib.auth as auth

from main_app.models import *


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
        category_names = [
            "Liquids",
            "Fruits"
        ]
        ingredient_data = [
            ("Water", 2, "Liquids"),
            ("Lemon", 8, "Fruits"),

        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1], category=Category.objects.get(name=n[2]))
                                        for n in ingredient_data])
        ingredients_list = ['Water', 'Lemon']
        quantities_list = ['1', '1']
        response = self.client.post('/recipe/new', {'name': 'Lemonade',
                                                    'description': 'water, but sour',
                                                    'recipe': '',
                                                    'ingredients': ingredients_list,
                                                    'quantities': quantities_list})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())
        self.assertEqual(response.url, '/recipe')


class AddRecipeViewTestNotLoggedUser(TestCase):
    def test_view_correct_redirection(self):
        response = self.client.get(reverse('add_recipe'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('add_recipe'), status_code=302,
                             target_status_code=200)


class AddIngredientViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ingredient/new')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add_ingredient'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_db_empty(self):
        response = self.client.get(reverse('add_ingredient'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/no_categories.html')

    def test_view_uses_correct_template_db_nonempty(self):
        category_names = [
            "Spices",
        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        response = self.client.get(reverse('add_ingredient'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/new_ingredient_form.html')

    def test_view_adds_ingredient(self):
        category_names = [
            "Liquids",
        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        response = self.client.post('/ingredient/new', {'name': 'water', 'price': '2', 'category': 'Liquids'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name='water').exists())
        self.assertEqual(response.url, '/ingredient')


class AddCategoryViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category/new')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add_category'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        category_names = [
            "Spices",
        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        response = self.client.get(reverse('add_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/new_category_form.html')

    def test_view_adds_category(self):
        response = self.client.post('/category/new', {'name': 'Spices'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Spices').exists())
        self.assertEqual(response.url, '/category')

    def test_view_aaaa(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
