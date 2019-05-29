from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *

from main_app.tests.TestSetupDatabase import *


# class UpdateRecipeViewTestSuperuser(TestCaseSuperuser):
#     def setUp(self):
#         TestDatabase.create_default_test_database()
#
#     def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
#         response = self.client.get('/recipe/999/update')
#         self.assertEqual(response.status_code, 404)
#
#     def test_view_url_exists_at_desired_location_id_exists(self):
#         item = Dish.objects.only('id').get(name='Lemonade').id
#         response = self.client.get('/recipe/{}/update'.format(item))
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_url_accessible_by_name(self):
#         item = Dish.objects.only('id').get(name='Lemonade').id
#         response = self.client.get(reverse('recipe_update', kwargs={'dish_id': item}))
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_updates_default_values(self):
#         item = Dish.objects.only('id').get(name='Lemonade').id
#         response = self.client.get(reverse('recipe_update', kwargs={'dish_id': item}))
#         self.assertEqual(response.context['form'].initial['name'], 'Lemonade')
#         self.assertTrue(Dish.objects.filter(id=item).exists())
#
#         # things should be deleted cascade
#         self.assertTrue(Ingredient.objects.filter(name='Water').exists())
#         self.assertFalse(Dish.objects.filter(name='Lemonade').exists())
#
#     def test_view_updates_properly_no_modifications(self):
#         item = Dish.objects.only('id').get(name='Lemonade').id
#         response = self.client.post(reverse('recipe_update', kwargs={'dish_id': item}))
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(Dish.objects.filter(id=item).exists())
#
#         # things should be deleted cascade
#         self.assertTrue(Ingredient.objects.filter(name='Water').exists())
#         self.assertFalse(Dish.objects.filter(name='Lemonade').exists())


class UpdateIngredientViewTestSuperuser(TestCaseSuperuser):
    def setUp(self):
        super().setUp()
        TestDatabase.create_default_test_database()

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999/update')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get('/ingredient/{}/update'.format(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_update', kwargs={'ing_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_updates_default_values(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_update', kwargs={'ing_id': item}))
        self.assertEqual(response.context['form'].initial['name'], 'Water')
        self.assertEqual(response.context['form'].initial['price'], 2)

    def test_view_updates_properly_no_modifications(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        ingredient_data={'name': 'Water',
                         'price': 2}
        response = self.client.post(reverse('ingredient_update', kwargs={'ing_id': item}),
                                    ingredient_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(id=item).exists())
        self.assertEquals(Ingredient.objects.get(id=item).name, 'Water')
        self.assertEquals(Ingredient.objects.get(id=item).price, 2)
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())
        self.assertTrue(Dish.objects.get(name='Lemonade').
                        ingredients.filter(name='Water').exists())

    def test_view_updates_properly_with_modifications(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        ingredient_data = {'name': 'Wine',
                           'price': 200}
        response = self.client.post(reverse('ingredient_update', kwargs={'ing_id': item}),
                                    ingredient_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(id=item).exists())
        self.assertEquals(Ingredient.objects.get(id=item).name, 'Wine')
        self.assertEquals(Ingredient.objects.get(id=item).price, 200)
        self.assertFalse(Ingredient.objects.filter(name='Water').exists())
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())
        self.assertTrue(Dish.objects.get(name='Lemonade').
                        ingredients.filter(name='Wine').exists())
