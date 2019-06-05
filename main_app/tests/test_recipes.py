from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *

from main_app.tests.TestSetupDatabase import *


# region add

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
        self.assertTrue(Recipe.objects.filter(name='Lemonade').exists())
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
        self.assertFalse(Recipe.objects.filter(name='Lemonade').exists())


# endregion
# region delete

class DeleteRecipeViewTestSuperuser(TestCaseSuperuser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database()

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/recipe/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = self.client.get('/recipe/{}/delete'.format(item))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_properly(self):
        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertTrue(Ingredient.objects.filter(name='Water').exists())
        self.assertFalse(Recipe.objects.filter(name='Lemonade').exists())

    def test_view_redirects_properly(self):
        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response, reverse('recipe'))


class DeleteRecipeViewTestNotSuperuser(TestCaseLoggedUser):
    @classmethod
    def setUpTestData(cls):
        ingredient_data = [
            ("Water", 2, True, True, True),
            ("Lemon", 8, True, True, True),
        ]
        TestDatabase.create_custom_test_database(ingredient_data=ingredient_data)

    def test_view_adds_and_deletes_recipe_owner(self):
        ingredients_list = ['Water', 'Lemon']
        quantities_list = ['1', '1']
        response = self.client.post('/recipe/new', {'name': 'Lemonade',
                                                    'description': 'water, but sour',
                                                    'recipe': 'hahaha to jest wymagane',
                                                    'ingredients': ingredients_list,
                                                    'quantities': quantities_list})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(name='Lemonade').exists())

        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertFalse(Recipe.objects.filter(name='Lemonade').exists())

    def test_view_deletes_recipe_not_logged_in(self):
        recipe_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        TestDatabase.create_custom_test_database(recipe_data=recipe_data)

        client = Client()
        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = client.get(reverse('recipe_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Recipe.objects.filter(name='Lemonade').exists())

    def test_view_deletes_recipe_not_logged_in_id_doesnt_exist(self):
        client = Client()
        response = client.get(reverse('recipe_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)

    def test_view_deletes_recipe_logged_in_not_owner(self):
        recipe_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        TestDatabase.create_custom_test_database(recipe_data=recipe_data)

        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Recipe.objects.filter(name='Lemonade').exists())

    def test_view_deletes_recipe_logged_in_not_owner_id_doesnt_exist(self):
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)


# endregion
# region getid

class RecipeIDViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ingredient_data = [
            ("Water", 2, True, True, True),
            ("Lemon", 8, True, True, True)

        ]
        recipe_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        TestDatabase.create_custom_test_database(ingredient_data=ingredient_data, recipe_data=recipe_data)

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/recipe/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = self.client.get('/recipe/{}'.format(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_id', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = Recipe.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_id', kwargs={'object_id': item}))
        self.assertTemplateUsed(response, 'food/recipe_id_get.html')

# endregion
# region update

# class UpdateRecipeViewTestSuperuser(TestCaseSuperuser):
#     def setUp(self):
#         TestDatabase.create_default_test_database()
#
#     def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
#         response = self.client.get('/recipe/999/update')
#         self.assertEqual(response.status_code, 404)
#
#     def test_view_url_exists_at_desired_location_id_exists(self):
#         item = Recipe.objects.only('id').get(name='Lemonade').id
#         response = self.client.get('/recipe/{}/update'.format(item))
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_url_accessible_by_name(self):
#         item = Recipe.objects.only('id').get(name='Lemonade').id
#         response = self.client.get(reverse('recipe_update', kwargs={'object_id': item}))
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_updates_default_values(self):
#         item = Recipe.objects.only('id').get(name='Lemonade').id
#         response = self.client.get(reverse('recipe_update', kwargs={'object_id': item}))
#         self.assertEqual(response.context['form'].initial['name'], 'Lemonade')
#         self.assertTrue(Recipe.objects.filter(id=item).exists())
#
#         # things should be deleted cascade
#         self.assertTrue(Ingredient.objects.filter(name='Water').exists())
#         self.assertFalse(Recipe.objects.filter(name='Lemonade').exists())
#
#     def test_view_updates_properly_no_modifications(self):
#         item = Recipe.objects.only('id').get(name='Lemonade').id
#         response = self.client.post(reverse('recipe_update', kwargs={'object_id': item}))
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(Recipe.objects.filter(id=item).exists())
#
#         # things should be deleted cascade
#         self.assertTrue(Ingredient.objects.filter(name='Water').exists())
#         self.assertFalse(Recipe.objects.filter(name='Lemonade').exists())

# endregion
