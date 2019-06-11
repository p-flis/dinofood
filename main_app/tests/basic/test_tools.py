from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *
from django.test import tag

from main_app.tests.TestSetupDatabase import *


# region add

@tag('cooking_tool', 'add', 'superuser')
class AddCookingToolViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/cooking_tool/new')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add_cooking_tool'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_cooking_tool'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/new_cooking_tool_form.html')

    def test_view_regular_add(self):
        response = self.client.post('/cooking_tool/new',
                                    {'name': 'Garnek'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CookingTool.objects.filter(name='Garnek').exists())
        self.assertEqual(response.url, '/cooking_tool')

    def test_view_correct_redirection(self):
        response = self.client.post('/cooking_tool/new',
                                    {'name': 'Garnek'},
                                    follow=True)
        self.assertRedirects(response,
                             reverse('cooking_tool'),
                             status_code=302,
                             target_status_code=200)


@tag('cooking_tool', 'add', 'normal_user')
class AddCookingToolViewTestNotLoggedIn(TestCase):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('add_cooking_tool'), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_cooking_tool'),
                             status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        response = self.client.post(reverse('add_cooking_tool'), {'name': 'Garnek'}, follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_cooking_tool'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(CookingTool.objects.filter(name='Garnek').exists())


@tag('cooking_tool', 'add', 'logged_user')
class AddCookingToolViewTestNotSuperuser(TestCaseLoggedUser):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('add_cooking_tool'), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_cooking_tool'),
                             status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        response = self.client.post(reverse('add_cooking_tool'), {'name': 'Garnek'}, follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('add_cooking_tool'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(CookingTool.objects.filter(name='Garnek').exists())


# endregion
# region delete

@tag('cooking_tool', 'delete', 'superuser')
class DeleteUnitViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/cooking_tool/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get('/cooking_tool/{}/delete'.format(item))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_properly(self):
        TestDatabase.create_default_test_database(tools=True, recipes=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertFalse(CookingTool.objects.filter(name='Garnek').exists())

    def test_view_redirects_properly(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response, reverse('cooking_tool'))


@tag('cooking_tool', 'delete', 'logged_user')
class DeleteCookingToolViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_deletes(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('cooking_tool_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(CookingTool.objects.filter(name='Garnek').exists())

    def test_view_deletes_id_doesnt_exist(self):
        response = self.client.get(reverse('cooking_tool_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('cooking_tool_delete',
                                                                                kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)


@tag('cooking_tool', 'delete', 'normal_user')
class DeleteCookingToolViewTestNormalUser(TestCase):
    def test_view_deletes(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('cooking_tool_delete',
                                                                                kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(CookingTool.objects.filter(name='Garnek').exists())

    def test_view_deletes_id_doesnt_exist(self):
        response = self.client.get(reverse('cooking_tool_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('cooking_tool_delete',
                                                                                kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)


# endregion
# region getid

@tag('cooking_tool', 'id', 'superuser')
class CookingToolIDViewTest(TestCaseSuperuser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(tools=True)

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/cooking_tool/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get('/cooking_tool/{}'.format(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_id', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_id', kwargs={'object_id': item}))
        self.assertTemplateUsed(response, 'food/cooking_tool_id_get.html')

    def test_view_correct_texts(self):
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_id', kwargs={'object_id': item}))
        self.assertContains(response, "Garnek")  # name


@tag('cooking_tool', 'id', 'normal_user')
class CookingToolIDViewTestNotLoggedIn(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(tools=True)

    def test_view_correct_redirection(self):
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_id', kwargs={'object_id': item}))
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('cooking_tool_id',
                                                                                kwargs={'object_id': item}))

    def test_view_correct_redirection_doesnt_exist(self):
        response = self.client.get(reverse('cooking_tool_id', kwargs={'object_id': 999}))
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('cooking_tool_id',
                                                                                kwargs={'object_id': 999}))


@tag('cooking_tool', 'delete', 'logged_user')
class CookingToolIDViewTestNotSuperuser(TestCaseLoggedUser):
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(tools=True)

    def test_view_correct_redirection(self):
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_id', kwargs={'object_id': item}))
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('cooking_tool_id',
                                                                                kwargs={'object_id': item}))

    def test_view_correct_redirection_doesnt_exist(self):
        response = self.client.get(reverse('cooking_tool_id', kwargs={'object_id': 999}))
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('cooking_tool_id',
                                                                                kwargs={'object_id': 999}))


# endregion
# region update


@tag('cooking_tool', 'update', 'superuser')
class UpdateCookingToolCookingToolViewTestSuperuser(TestCaseSuperuser):
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/cooking_tool/999/update')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get('/cooking_tool/{}/update'.format(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_update', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_updates_default_values(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_update', kwargs={'object_id': item}))
        self.assertEqual(response.context['form'].initial['name'], 'Garnek')

    def test_view_updates_properly_no_modifications(self):
        TestDatabase.create_default_test_database(tools=True, recipes=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response_get = self.client.get(reverse('cooking_tool_update', kwargs={'object_id': item}))
        cooking_tool_data = response_get.context['form'].initial
        response = self.client.post(reverse('cooking_tool_update', kwargs={'object_id': item}),
                                    cooking_tool_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CookingTool.objects.filter(id=item).exists())
        self.assertEquals(CookingTool.objects.get(id=item).name, 'Garnek')
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertTrue(Recipe.objects.get(name='Lemoniada').
                        tools.filter(name='Garnek').exists())

    def test_view_updates_properly_with_modifications(self):
        TestDatabase.create_default_test_database(units=True, tools=True, ingredients=True, recipes=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response_get = self.client.get(reverse('cooking_tool_update', kwargs={'object_id': item}))
        cooking_tool_data = response_get.context['form'].initial
        cooking_tool_data['name'] = "Durszlak"
        response = self.client.post(reverse('cooking_tool_update', kwargs={'object_id': item}),
                                    cooking_tool_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CookingTool.objects.filter(id=item).exists())
        self.assertEquals(CookingTool.objects.get(id=item).name, 'Durszlak')
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertTrue(Recipe.objects.get(name='Lemoniada').
                        tools.filter(name='Durszlak').exists())


@tag('cooking_tool', 'update', 'logged_user')
class UpdateUnitViewTestNotSuperuser(TestCaseLoggedUser):
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get(reverse('cooking_tool_update', kwargs={'object_id': 999}))
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'cooking_tool_update',
                                 kwargs={'object_id': 999}))

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_update', kwargs={'object_id': item}))
        self.assertRedirects(response,
                             reverse('cooking_tool_update', kwargs={'object_id': item}) + "?next=" + reverse(
                                 'ingredient_id',
                                 kwargs={'object_id': item}))
    # todo post?


@tag('cooking_tool', 'update', 'normal_user')
class UpdateIngredientViewTestNotLoggedIn(TestCase):
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get(reverse('cooking_tool_update', kwargs={'object_id': 999}))
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'cooking_tool_update',
                                 kwargs={'object_id': 999}))

    def test_view_url_exists_at_desired_location_id_exists(self):
        TestDatabase.create_default_test_database(tools=True)
        item = CookingTool.objects.only('id').get(name='Garnek').id
        response = self.client.get(reverse('cooking_tool_update', kwargs={'object_id': item}))
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse(
                                 'cooking_tool_update',
                                 kwargs={'object_id': item}))
    # todo post?
# endregion
