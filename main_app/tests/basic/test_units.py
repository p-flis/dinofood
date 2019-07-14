from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *
from django.test import tag
from unittest import skip

from main_app.tests.TestSetupDatabase import *


# region add

@tag('unit', 'add', 'superuser')
class AddUnitViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/unit/new')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add_ingredient'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_unit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/unit_form.html')

    def test_view_regular_add(self):
        response = self.client.post(reverse('add_unit'),
                                    {'name': 'Gram',
                                     'amount': 100})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Unit.objects.filter(name='Gram').exists())
        self.assertEqual(response.url, '/unit/')

    def test_view_correct_redirection(self):
        response = self.client.post(reverse('add_unit'),
                                    {'name': 'Gram',
                                     'amount': 100},
                                    follow=True)
        self.assertRedirects(response,
                             reverse('unit'),
                             status_code=302,
                             target_status_code=200)


@tag('unit', 'add', 'normal_user')
class AddUnitViewTestNormalUser(TestCase):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('add_unit'), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_unit'),
                             status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        response = self.client.post(reverse('add_unit'), {'name': 'Gram', 'amount': 100}, follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_unit'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(Unit.objects.filter(name='Gram').exists())


@tag('unit', 'add', 'logged_user')
class AddUnitViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('add_unit'), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_unit'),
                             status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        response = self.client.post(reverse('add_unit'), {'name': 'Gram', 'amount': 100}, follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_unit'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(Unit.objects.filter(name='Gram').exists())


# endregion
# region delete

@skip
@tag('unit', 'delete', 'superuser')
class DeleteUnitViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/unit/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Gram').id
        response = self.client.get('/unit/'+str(item.id)+'/delete')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Gram').id
        response = self.client.get(reverse('unit_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_properly(self):
        TestDatabase.create_default_test_database(units=True, ingredients=True, recipes=True, tools=True)
        item = Unit.objects.only('id').get(name='Gram').id
        response = self.client.get(reverse('unit_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertTrue(Ingredient.objects.filter(name='Woda').exists())
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertFalse(Unit.objects.filter(name='Gram').exists())

    def test_view_redirects_properly(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Gram').id
        response = self.client.get(reverse('unit_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response, reverse('unit'))


@tag('unit', 'delete', 'logged_user')
class DeleteUnitViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_deletes(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Gram').id
        response = self.client.get(reverse('unit_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('unit_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Unit.objects.filter(name='Gram').exists())

    def test_view_deletes_doesnt_exist(self):
        response = self.client.get(reverse('unit_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('unit_delete',
                                                                                kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)


@tag('unit', 'delete', 'logged_user')
class DeleteUnitViewTestNormalUser(TestCase):
    def test_view_deletes(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Gram').id
        response = self.client.get(reverse('unit_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('unit_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Unit.objects.filter(name='Gram').exists())

    def test_view_deletes_doesnt_exist(self):
        response = self.client.get(reverse('unit_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('unit_delete',
                                                                                kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)


# endregion
# region getid

@tag('unit', 'id', 'superuser')
class UnitIDViewTest(TestCaseSuperuser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(units=True)

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/unit/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Unit.objects.only('id').get(name='Gram').id
        response = self.client.get('/unit/' + str(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Unit.objects.only('id').get(name='Gram').id
        response = self.client.get(reverse('unit_id', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = Unit.objects.only('id').get(name='Gram').id
        response = self.client.get(reverse('unit_id', kwargs={'object_id': item}))
        self.assertTemplateUsed(response, 'main_app/unit_detail.html')

    def test_view_correct_texts(self):
        item = Unit.objects.only('id').get(name='Kilogram').id
        response = self.client.get(reverse('unit_id', kwargs={'object_id': item}))
        self.assertContains(response, "10")  # amount
        self.assertContains(response, "Kilogram")  # name


@tag('unit', 'id', 'normal_user')
class UnitIDViewTestNormalUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(units=True)

    def test_view_correct_redirection(self):
        item = Unit.objects.only('id').get(name='Kilogram').id
        response = self.client.get(reverse('unit_id', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('unit_id',
                                                                                kwargs={'object_id': item}))

    def test_view_correct_redirection_doesnt_exist(self):
        response = self.client.get(reverse('unit_id', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('unit_id',
                                                                                kwargs={'object_id': 999}))


@tag('unit', 'id', 'logged_user')
class UnitIDViewTestLoggedUser(TestCaseLoggedUser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(units=True)

    def test_view_correct_redirection(self):
        item = Unit.objects.only('id').get(name='Kilogram').id
        response = self.client.get(reverse('unit_id', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('unit_id',
                                                                                kwargs={'object_id': item}))

    def test_view_correct_redirection_doesnt_exist(self):
        response = self.client.get(reverse('unit_id', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('unit_id',
                                                                                kwargs={'object_id': 999}))


# endregion
# region update


@tag('unit', 'update', 'superuser')
class UpdateUnitViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/unit/999/update')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Kilogram').id
        response = self.client.get('/unit/'+str(item)+'/update')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Kilogram').id
        response = self.client.get(reverse('unit_update', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_updates_default_values(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Kilogram').id
        response = self.client.get(reverse('unit_update', kwargs={'object_id': item}))
        self.assertEqual(response.context['form'].initial['name'], 'Kilogram')
        self.assertEqual(response.context['form'].initial['amount'], 10)

    def test_view_updates_properly_no_modifications(self):
        TestDatabase.create_default_test_database(units=True, ingredients=True, recipes=True)
        item = Unit.objects.only('id').get(name='Kilogram').id
        response_get = self.client.get(reverse('unit_update', kwargs={'object_id': item}))
        unit_data = response_get.context['form'].initial
        response = self.client.post(reverse('unit_update', kwargs={'object_id': item}),
                                    unit_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Unit.objects.filter(id=item).exists())
        self.assertEquals(Unit.objects.get(id=item).name, 'Kilogram')
        self.assertEquals(Unit.objects.get(id=item).amount, 10)

        self.assertTrue(Ingredient.objects.filter(name='Woda').exists())
        self.assertTrue(Ingredient.objects.get(name='Woda').
                        units.filter(name='Kilogram').exists())
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertTrue(Recipe.objects.get(name='Lemoniada').
                        ingredients.filter(name='Cytryna').exists())
        self.assertTrue(Recipe.objects.filter(name='Lemoniada',
                                              recipeingredient__ingredient__name='Cytryna',
                                              recipeingredient__unit__name='Kilogram'))

    def test_view_updates_properly_with_modifications(self):
        TestDatabase.create_default_test_database(units=True, ingredients=True, recipes=True)
        item = Unit.objects.only('id').get(name='Kilogram').id
        response_get = self.client.get(reverse('unit_update', kwargs={'object_id': item}))
        unit_data = response_get.context['form'].initial
        unit_data['name'] = "Litr"
        unit_data['amount'] = 50
        response = self.client.post(reverse('unit_update', kwargs={'object_id': item}),
                                    unit_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Unit.objects.filter(id=item).exists())
        self.assertEquals(Unit.objects.get(id=item).name, 'Litr')
        self.assertEquals(Unit.objects.get(id=item).amount, 50)

        self.assertTrue(Ingredient.objects.filter(name='Woda').exists())
        self.assertFalse(Ingredient.objects.get(name='Woda').
                         units.filter(name='Kilogram').exists())
        self.assertTrue(Ingredient.objects.get(name='Woda').
                        units.filter(name='Litr').exists())
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertTrue(Recipe.objects.get(name='Lemoniada').
                        ingredients.filter(name='Cytryna').exists())
        self.assertTrue(Recipe.objects.filter(name='Lemoniada',
                                              recipeingredient__ingredient__name='Cytryna',
                                              recipeingredient__unit__name='Litr'))


@tag('unit', 'update', 'logged_user')
class UpdateUnitViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_doesnt_exists(self):
        response = self.client.get(reverse('unit_update', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'unit_update',
                                 kwargs={'object_id': 999}))

    def test_view(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Kilogram').id
        response = self.client.get(reverse('unit_update', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'unit_update',
                                 kwargs={'object_id': item}))
    # todo post?


@tag('unit', 'update', 'normal_user')
class UpdateUnitViewTestNormalUser(TestCase):
    def test_view_doesnt_exists(self):
        response = self.client.get(reverse('unit_update', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'unit_update',
                                 kwargs={'object_id': 999}))

    def test_view(self):
        TestDatabase.create_default_test_database(units=True)
        item = Unit.objects.only('id').get(name='Kilogram').id
        response = self.client.get(reverse('unit_update', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'unit_update',
                                 kwargs={'object_id': item}))
    # todo post?
# endregion
