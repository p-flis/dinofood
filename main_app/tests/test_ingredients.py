from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *

from main_app.tests.TestSetupDatabase import *


# region add

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
        response = self.client.post('/ingredient/new',
                                    {'name': 'water', 'price': '2', 'is_vegetarian': 'false', 'is_vegan': 'false',
                                     'is_gluten_free': 'false'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name='water').exists())
        self.assertEqual(response.url, '/ingredient')

    def test_view_adds_ingredient_redirect(self):
        response = self.client.post('/ingredient/new',
                                    {'name': 'water', 'price': '2', 'is_vegetarian': 'false', 'is_vegan': 'false',
                                     'is_gluten_free': 'false'}, follow=True)
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


# endregion
# region delete

class DeleteIngredientViewTestSuperuser(TestCaseSuperuser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database()

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get('/ingredient/{}/delete'.format(item))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_properly(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertFalse(Ingredient.objects.filter(name='Water').exists())
        self.assertFalse(Dish.objects.filter(name='Lemonade').exists())

    def test_view_redirects_properly(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response, reverse('ingredient'))


class DeleteIngredientViewTestNotSuperuser(TestCaseLoggedUser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database()

    def test_view_deletes_ingredient_not_logged_in(self):
        client = Client()
        item = Ingredient.objects.only('id').get(name='Water').id
        response = client.get(reverse('ingredient_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Ingredient.objects.filter(name='Water').exists())
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())

    def test_view_deletes_ingredient_not_logged_in_id_doesnt_exist(self):
        client = Client()
        response = client.get(reverse('ingredient_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)

    def test_view_deletes_ingredient_logged_in(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Ingredient.objects.filter(name='Water').exists())
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())

    def test_view_deletes_ingredient_logged_in_id_doesnt_exist(self):
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)


# endregion
# region getid

class IngredientIDViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ingredient_data = [
            ("Water", 2, True, True, True),
        ]
        TestDatabase.create_custom_test_database(ingredient_data=ingredient_data)

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        response = self.client.get('/ingredient/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}))
        self.assertTemplateUsed(response, 'food/ingredient_id_get.html')


# endregion
# region update

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
        response = self.client.get(reverse('ingredient_update', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_updates_default_values(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_update', kwargs={'object_id': item}))
        self.assertEqual(response.context['form'].initial['name'], 'Water')
        self.assertEqual(response.context['form'].initial['price'], 2)

    def test_view_updates_properly_no_modifications(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        ingredient_data = {'name': 'Water',
                           'price': 2}
        response = self.client.post(reverse('ingredient_update', kwargs={'object_id': item}),
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
        response = self.client.post(reverse('ingredient_update', kwargs={'object_id': item}),
                                    ingredient_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(id=item).exists())
        self.assertEquals(Ingredient.objects.get(id=item).name, 'Wine')
        self.assertEquals(Ingredient.objects.get(id=item).price, 200)
        self.assertFalse(Ingredient.objects.filter(name='Water').exists())
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())
        self.assertTrue(Dish.objects.get(name='Lemonade').
                        ingredients.filter(name='Wine').exists())

# endregion
