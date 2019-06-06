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
                                    {'name': 'water',
                                     'price': '2',
                                     'is_vegetarian': 'false',
                                     'is_vegan': 'false',
                                     'is_gluten_free': 'false',
                                     'units':[]})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name='water').exists())
        self.assertEqual(response.url, '/ingredient')

    def test_view_adds_ingredient_redirect(self):
        response = self.client.post('/ingredient/new',
                                    {'name': 'water',
                                     'price': '2',
                                     'is_vegetarian': 'false',
                                     'is_vegan': 'false',
                                     'is_gluten_free': 'false'},
                                    follow=True)
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
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get('/ingredient/{}/delete'.format(item))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_properly(self):
        TestDatabase.create_default_test_database(units=True, ingredients=True, recipes=True, tools=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertFalse(Ingredient.objects.filter(name='Woda').exists())
        self.assertFalse(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertTrue(Unit.objects.filter(name='Gram').exists())

    def test_view_redirects_properly(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response, reverse('ingredient'))


class DeleteIngredientViewTestNotSuperuser(TestCaseLoggedUser):
    def test_view_deletes_ingredient_not_logged_in(self):
        TestDatabase.create_default_test_database(ingredients=True)
        client = Client()
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = client.get(reverse('ingredient_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Ingredient.objects.filter(name='Woda').exists())

    def test_view_deletes_ingredient_not_logged_in_id_doesnt_exist(self):
        client = Client()
        response = client.get(reverse('ingredient_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)

    def test_view_deletes_ingredient_logged_in(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Ingredient.objects.filter(name='Woda').exists())

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
        TestDatabase.create_default_test_database(ingredients=True)

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get('/ingredient/{}'.format(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}))
        self.assertTemplateUsed(response, 'food/ingredient_id_get.html')

    def test_view_correct_texts(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}))
        self.assertContains(response, "Woda")

# endregion
# region update


class UpdateIngredientViewTestSuperuser(TestCaseSuperuser):
    def setUp(self):
        super().setUp()

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999/update')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get('/ingredient/{}/update'.format(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_update', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_updates_default_values(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_update', kwargs={'object_id': item}))
        self.assertEqual(response.context['form'].initial['name'], 'Woda')
        self.assertEqual(response.context['form'].initial['price'], 2)

    def test_view_updates_properly_no_modifications(self):
        TestDatabase.create_default_test_database(units=True, ingredients=True, recipes=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response_get = self.client.get(reverse('ingredient_update', kwargs={'object_id': item}))
        ingredient_data = response_get.context['form'].initial
        response = self.client.post(reverse('ingredient_update', kwargs={'object_id': item}),
                                    ingredient_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(id=item).exists())
        self.assertEquals(Ingredient.objects.get(id=item).name, 'Woda')
        self.assertEquals(Ingredient.objects.get(id=item).price, 2)
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertTrue(Unit.objects.filter(name='Gram').exists())
        self.assertTrue(Recipe.objects.get(name='Lemoniada').
                        ingredients.filter(name='Woda').exists())

    def test_view_updates_properly_with_modifications(self):
        TestDatabase.create_default_test_database(units=True, ingredients=True, recipes=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response_get = self.client.get(reverse('ingredient_update', kwargs={'object_id': item}))
        ingredient_data = response_get.context['form'].initial
        ingredient_data['name'] = 'Wino'
        ingredient_data['price'] = 20
        #a workaround, because we get objects with GET, and need only ids in POST
        new_units = []
        for value in ingredient_data['units']:
            new_units.append(value.id)
        ingredient_data['units'] = new_units
        #end of workaround
        response = self.client.post(reverse('ingredient_update', kwargs={'object_id': item}),
                                    ingredient_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(id=item).exists())
        self.assertNotEquals(Ingredient.objects.get(id=item).name, 'Woda')
        self.assertEquals(Ingredient.objects.get(id=item).name, 'Wino')
        self.assertEquals(Ingredient.objects.get(id=item).price, 20)
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertTrue(Unit.objects.filter(name='Gram').exists())
        self.assertTrue(Recipe.objects.get(name='Lemoniada').
                        ingredients.filter(name='Wino').exists())

# endregion
