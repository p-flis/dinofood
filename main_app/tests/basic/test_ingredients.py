from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *
from django.test import tag
from unittest import skip

from main_app.tests.TestSetupDatabase import *


# region add
@tag('ingredient', 'add', 'superuser')
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
        self.assertTemplateUsed(response, 'main_app/ingredient_form.html')

    def test_view_adds_ingredient(self):
        response = self.client.post(reverse('add_ingredient'),
                                    {'name': 'water',
                                     'price': '2',
                                     'is_vegetarian': 'false',
                                     'is_vegan': 'false',
                                     'is_gluten_free': 'false',
                                     'units': []})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name='water').exists())
        self.assertEqual(response.url, '/ingredient/')

    def test_view_adds_ingredient_redirect(self):
        response = self.client.post(reverse('add_ingredient'),
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


@tag('ingredient', 'add', 'normal_user')
class AddIngredientViewTestNormalUser(TestCase):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('add_ingredient'), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_ingredient'),
                             status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        response = self.client.post(reverse('add_ingredient'), {'name': 'water', 'price': '2'}, follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_ingredient'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(Ingredient.objects.filter(name='water').exists())


@tag('ingredient', 'add', 'logged_user')
class AddIngredientViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('add_ingredient'), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_ingredient'),
                             status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        response = self.client.post(reverse('add_ingredient'), {'name': 'water', 'price': '2'}, follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_ingredient'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(Ingredient.objects.filter(name='water').exists())


# endregion
# region delete

@skip
@tag('ingredient', 'delete', 'superuser')
class DeleteIngredientViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get('/ingredient/' + str(item) + '/delete')
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


@tag('ingredient', 'delete', 'logged_user')
class DeleteIngredientViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_deletes(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Ingredient.objects.filter(name='Woda').exists())

    def test_view_deletes_id_doesnt_exist(self):
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)


@tag('ingredient', 'delete', 'normal_user')
class DeleteIngredientViewTestNormalUser(TestCase):
    def test_view_deletes(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Ingredient.objects.filter(name='Woda').exists())

    def test_view_deletes_id_doesnt_exist(self):
        response = self.client.get(reverse('ingredient_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete',
                                                                                kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)


# endregion
# region getid


@tag('ingredient', 'id', 'superuser')
class IngredientIDViewTest(TestCaseSuperuser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(ingredients=True, units=True)

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get('/ingredient/' + str(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}))
        self.assertTemplateUsed(response, 'main_app/ingredient_detail.html')

    def test_view_correct_texts(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}))
        self.assertContains(response, "Woda")
        self.assertContains(response, "Gram")


@tag('ingredient', 'id', 'normal_user')
class IngredientIDViewTestNormalUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(ingredients=True, units=True)

    def test_view_correct_redirection(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_id',
                                                                                kwargs={'object_id': item}))

    def test_view_correct_redirection_doesnt_exist(self):
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_id',
                                                                                kwargs={'object_id': 999}))


@tag('ingredient', 'id', 'logged_user')
class IngredientIDViewTestLoggedUser(TestCaseLoggedUser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(ingredients=True, units=True)

    def test_view_correct_redirection(self):
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_id',
                                                                                kwargs={'object_id': item}))

    def test_view_correct_redirection_doesnt_exist(self):
        response = self.client.get(reverse('ingredient_id', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_id',
                                                                                kwargs={'object_id': 999}))


# endregion
# region update


@skip
@tag('ingredient', 'update', 'superuser')
class UpdateIngredientViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999/update')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get('/ingredient/' + str(item) + '/update')
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
        self.assertTrue(Ingredient.objects.get(name='Woda').
                        units.filter(name='Gram').exists())
        # lemoniada.woda.unit.name=gram

    def test_view_updates_properly_with_modifications(self):
        TestDatabase.create_default_test_database(units=True, ingredients=True, recipes=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response_get = self.client.get(reverse('ingredient_update', kwargs={'object_id': item}))
        ingredient_data = response_get.context['form'].initial
        ingredient_data['name'] = 'Wino'
        ingredient_data['price'] = 20
        # a workaround, because we get objects with GET, and need only ids in POST
        new_units = []
        for value in ingredient_data['units']:
            new_units.append(value.id)
        ingredient_data['units'] = new_units
        # end of workaround
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
        self.assertTrue(Ingredient.objects.get(name='Wino').
                        units.filter(name='Gram').exists())
        # lemoniada.woda.unit.name=gram
        # todo what to da after change of units? - lemoniada.woda.unit to default & force to change it manually?


@tag('ingredient', 'update', 'logged_user')
class UpdateIngredientViewTestLoggedUser(TestCaseLoggedUser):  # todo post
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999/update', follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'ingredient_update',
                                 kwargs={'object_id': 999}))

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get('/ingredient/'+str(item)+'/update', follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'ingredient_update',
                                 kwargs={'object_id': item}))


@tag('ingredient', 'update', 'normal_user')
class UpdateIngredientViewTestNormalUser(TestCase):  # todo post
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999/update', follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'ingredient_update',
                                 kwargs={'object_id': 999}))

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(ingredients=True)
        item = Ingredient.objects.only('id').get(name='Woda').id
        response = self.client.get('/ingredient/'+str(item)+'/update', follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'ingredient_update',
                                 kwargs={'object_id': item}))

@tag('ingredient', 'fridge', 'logged_user')
class FridgeViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/fridge')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('fridge'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('fridge'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/fridge.html')

    #WHY IT DOES NOT WORK?!
    def test_view_regular_change(self):
        TestDatabase.create_default_test_database(ingredients=True)
        fridge = [x.id for x in Ingredient.objects.all()]
        response = self.client.post(reverse('fridge'),
                                    {'ingredients': fridge})
        request = response.wsgi_request
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(request.user.ingredients.all(), Ingredient.objects.all(), transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(response.url, '/recipe/')

@tag('ingedient', 'fridge', 'normal_user')
class FridgeViewTestNormalUser(TestCase):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('fridge'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('fridge'), status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        TestDatabase.create_default_test_database(tools=True)
        tools_list = [CookingTool.objects.first()]
        response = self.client.post(reverse('fridge'),
                                    {'fridge': tools_list},
                                    follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('fridge'), status_code=302,
                             target_status_code=200)
# endregion
