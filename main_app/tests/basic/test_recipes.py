from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *
from django.test import tag
from django.forms.formsets import formset_factory
from main_app.tests.TestSetupDatabase import *
from accounts.models import *
from main_app.forms import *
from unittest import skip

# region add
@tag('recipe', 'add', 'logged_user')
class AddRecipeViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipe/new')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add_recipe'))
        self.assertTemplateUsed(response, 'main_app/recipe_form.html')

    def test_view_adds_recipe(self):
        TestDatabase.create_default_test_database(ingredients=True, tools=True, units=True)
        tools_list = [CookingTool.objects.first().id]
        response = self.client.post(reverse('add_recipe'), {'name': 'Lemoniada',
                                                    'description': 'Woda, ale słodka',
                                                    'recipe_text': 'hahaha to jest wymagane',
                                                    'form-TOTAL_FORMS': ['1'],
                                                    'form-INITIAL_FORMS': ['0'],
                                                    'form-MIN_NUM_FORMS': ['1'],
                                                    'form-MAX_NUM_FORMS': ['1000'],
                                                    'form-0-ingredient': Ingredient.objects.get(name='Cytryna').id,
                                                    'form-0-quantity': ['122'],
                                                    'form-0-unit': Unit.objects.get(name='Gram').id,
                                                    'tools': tools_list,
                                                    'image': 'default.png'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())
        self.assertEqual(response.url, '/recipe/')

    def test_view_adds_recipe_redirect(self):
        TestDatabase.create_default_test_database(ingredients=True, tools=True, units=True)
        tools_list = [CookingTool.objects.first().id]
        response = self.client.post(reverse('add_recipe'), {'name': 'Lemoniada',
                                                    'description': 'Woda, ale słodka',
                                                    'recipe_text': 'hahaha to jest wymagane',
                                                    'form-TOTAL_FORMS': ['1'],
                                                    'form-INITIAL_FORMS': ['0'],
                                                    'form-MIN_NUM_FORMS': ['1'],
                                                    'form-MAX_NUM_FORMS': ['1000'],
                                                    'form-0-ingredient': Ingredient.objects.get(name='Cytryna').id,
                                                    'form-0-quantity': ['122'],
                                                    'form-0-unit': Unit.objects.get(name='Gram').id,
                                                    'tools': tools_list,
                                                    'image': 'default.png'},
                                                    follow=True)
        self.assertRedirects(response, reverse('recipe'), status_code=302, target_status_code=200)


@tag('recipe', 'add', 'normal_user')
class AddRecipeViewTestNotLoggedUser(TestCase):
    def test_view_correct_redirection_get(self):
        response = self.client.get(reverse('add_recipe'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('add_recipe'), status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_post(self):
        TestDatabase.create_default_test_database(ingredients=True, tools=True, units=True)
        tools_list = [CookingTool.objects.first().id]
        response = self.client.post(reverse('add_recipe'), {'name': 'Lemoniada',
                                                    'description': 'Woda, ale słodka',
                                                    'recipe_text': 'hahaha to jest wymagane',
                                                    'form-TOTAL_FORMS': ['1'],
                                                    'form-INITIAL_FORMS': ['0'],
                                                    'form-MIN_NUM_FORMS': ['1'],
                                                    'form-MAX_NUM_FORMS': ['1000'],
                                                    'form-0-ingredient': Ingredient.objects.get(name='Cytryna').id,
                                                    'form-0-quantity': ['122'],
                                                    'form-0-unit': Unit.objects.get(name='Gram').id,
                                                    'tools': tools_list,
                                                    'image': 'default.png'},
                                                    follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('add_recipe'), status_code=302,
                             target_status_code=200)
        self.assertFalse(Recipe.objects.filter(name='Lemoniada').exists())


# endregion
# region delete

@skip
@tag('recipe', 'delete', 'superuser')
class DeleteRecipeViewTestSuperuser(TestCaseSuperuser):
    def setUp(self):
        super().setUp()
        TestDatabase.create_default_test_database(recipes=True, ingredients=True, units=True, tools=True)

    def test_view_doesnt_exists(self):
        response = self.client.get(reverse('recipe_delete', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_view(self):
        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_delete', args=[item]))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_properly(self):
        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name='Woda').exists())
        self.assertTrue(CookingTool.objects.filter(name='Garnek').exists())
        self.assertFalse(Recipe.objects.filter(name='Lemoniada').exists())

    def test_view_redirects_properly(self):
        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response, reverse('recipe'))


@skip
@tag('recipe', 'delete', 'logged_user')
class DeleteRecipeViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_deletes_owner(self):  # todo dodać przez bazę danych, nie przez post
        TestDatabase.create_default_test_database(ingredients=True, tools=True, units=True)
        tools_list = [CookingTool.objects.first().id]
        response = self.client.post(reverse('add_recipe'), {'name': 'Lemoniada',
                                                    'description': 'Woda, ale słodka',
                                                    'recipe_text': 'hahaha to jest wymagane',
                                                    'form-TOTAL_FORMS': ['1'],
                                                    'form-INITIAL_FORMS': ['0'],
                                                    'form-MIN_NUM_FORMS': ['1'],
                                                    'form-MAX_NUM_FORMS': ['1000'],
                                                    'form-0-ingredient': Ingredient.objects.get(name='Cytryna').id,
                                                    'form-0-quantity': ['122'],
                                                    'form-0-unit': Unit.objects.get(name='Gram').id,
                                                    'tools': tools_list,
                                                    'image': 'default.png'},
                                                    follow=True)
        self.assertRedirects(response, reverse('recipe'), status_code=302, target_status_code=200)

        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertFalse(Recipe.objects.filter(name='Lemoniada').exists())

    def test_view_deletes(self):
        TestDatabase.create_default_test_database(recipes=True)

        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())

    def test_view_deletes_id_doesnt_exist(self):
        response = self.client.get(reverse('recipe_delete', kwargs={'object_id': 999}))
        self.assertEqual(response.status_code, 404)


@tag('recipe', 'delete', 'normal_user')
class DeleteRecipeViewTestNormalUser(TestCase):
    def test_view_deletes(self):
        TestDatabase.create_default_test_database(recipes=True)

        client = Client()
        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = client.get(reverse('recipe_delete', kwargs={'object_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'object_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Recipe.objects.filter(name='Lemoniada').exists())

    def test_view_deletes_id_doesnt_exist(self):
        client = Client()
        response = client.get(reverse('recipe_delete', kwargs={'object_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'object_id': 999}),
                             status_code=302,
                             target_status_code=200)


# endregion
# region getid

@tag('recipe', 'id', 'normal_user')
class RecipeIDViewTest(TestCase):  # todo logged user?
    @classmethod
    def setUpTestData(cls):
        TestDatabase.create_default_test_database(ingredients=True, units=True, recipes=True, tools=True)

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/recipe/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get('/recipe/'+str(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_id', kwargs={'object_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_id', kwargs={'object_id': item}))
        self.assertTemplateUsed(response, 'main_app/recipe_detail.html')

    def test_view_displays_everything(self):
        item = Recipe.objects.only('id').get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_id', kwargs={'object_id': item}))
        self.assertContains(response, 'Lemoniada')  # name
        self.assertContains(response, 'Woda, ale słodka')  # description
        self.assertContains(response, 'Domyśl się')  # recipe_text
        self.assertContains(response, 'Woda')  # ingredient
        self.assertContains(response, 'Garnek')  # tool

@tag('recipe', 'accept', 'super_user')
class AcceptRecipeViewTestSuperUser(TestCaseSuperuser):

    def test_view_new_recipe_is_accepted_super_user(self):
        TestDatabase.create_default_test_database(ingredients=True, tools=True, units=True)
        tools_list = [CookingTool.objects.first().id]
        response = self.client.post(reverse('add_recipe'), {'name': 'Lemoniada',
                                                    'description': 'Woda, ale słodka',
                                                    'recipe_text': 'hahaha to jest wymagane',
                                                    'form-TOTAL_FORMS': ['1'],
                                                    'form-INITIAL_FORMS': ['0'],
                                                    'form-MIN_NUM_FORMS': ['1'],
                                                    'form-MAX_NUM_FORMS': ['1000'],
                                                    'form-0-ingredient': Ingredient.objects.get(name='Cytryna').id,
                                                    'form-0-quantity': ['122'],
                                                    'form-0-unit': Unit.objects.get(name='Gram').id,
                                                    'tools': tools_list,
                                                    'image': 'default.png'},
                                    follow=True)
        self.assertTrue(Recipe.objects.filter(name='Lemoniada')[0].accepted)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('accept_recipes'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('accept_recipes'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('accept_recipes'))
        self.assertTemplateUsed(response, 'main_app/recipe_list.html')

    def test_view_recipe_id_accept(self):
        TestDatabase.create_default_test_database(recipes=True)
        item = Recipe.objects.filter(name='Lemoniada')[0]
        item.accepted=False
        item.save()
        self.assertFalse(Recipe.objects.filter(name='Lemoniada')[0].accepted)
        response = self.client.get(reverse('recipe_accept', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(name='Lemoniada')[0].accepted)

    def test_view_recipe_id_accept_id_not_exists(self):
        response = self.client.get(reverse('recipe_accept', args=[999]))
        self.assertEqual(response.status_code, 404)


@tag('recipe', 'accept', 'logged_user')
class AcceptRecipeViewTestLoggedUser(TestCaseLoggedUser):
    def test_view_new_recipe_normal_user(self):
        TestDatabase.create_default_test_database(ingredients=True, tools=True, units=True)
        tools_list = [CookingTool.objects.first().id]
        response = self.client.post(reverse('add_recipe'), {'name': 'Lemoniada',
                                                    'description': 'Woda, ale słodka',
                                                    'recipe_text': 'hahaha to jest wymagane',
                                                    'form-TOTAL_FORMS': ['1'],
                                                    'form-INITIAL_FORMS': ['0'],
                                                    'form-MIN_NUM_FORMS': ['1'],
                                                    'form-MAX_NUM_FORMS': ['1000'],
                                                    'form-0-ingredient': Ingredient.objects.get(name='Cytryna').id,
                                                    'form-0-quantity': ['122'],
                                                    'form-0-unit': Unit.objects.get(name='Gram').id,
                                                    'tools': tools_list,
                                                    'image': 'default.png'},
                                                    follow=True)
        self.assertFalse(Recipe.objects.filter(name='Lemoniada')[0].accepted)

    def test_view_logged_user_is_redirected(self):
        response = self.client.get(reverse('accept_recipes'))
        self.assertEqual(response.status_code, 302)

    def test_view_logged_user_is_redirected(self):
        response = self.client.get(reverse('recipe_accept', args=[999]))
        self.assertEqual(response.status_code, 302)

# not sure about image tests


# endregion
# region update
# todo region update
# below needs to be corrected

# class UpdateRecipeViewTestSuperuser(TestCaseSuperuser):
#     def setUp(self):
#         TestDatabase.create_default_test_database()
#
#     def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
#         response = self.client.get(reverse('recipe_update', args=[999]))
#         self.assertEqual(response.status_code, 404)
#
#     def test_view_url_exists_at_desired_location_id_exists(self):
#         item = Recipe.objects.only('id').get(name='Lemoniada').id
#         response = self.client.get(reverse('recipe_update', args=[item]))
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_url_accessible_by_name(self):
#         item = Recipe.objects.only('id').get(name='Lemoniada').id
#         response = self.client.get(reverse('recipe_update', kwargs={'object_id': item}))
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_updates_default_values(self):
#         item = Recipe.objects.only('id').get(name='Lemoniada').id
#         response = self.client.get(reverse('recipe_update', kwargs={'object_id': item}))
#         self.assertEqual(response.context['form'].initial['name'], 'Lemoniada')
#         self.assertTrue(Recipe.objects.filter(id=item).exists())
#
#         # things should be deleted cascade
#         self.assertTrue(Ingredient.objects.filter(name='Woda').exists())
#         self.assertFalse(Recipe.objects.filter(name='Lemoniada').exists())
#
#     def test_view_updates_properly_no_modifications(self):
#         item = Recipe.objects.only('id').get(name='Lemoniada').id
#         response = self.client.post(reverse('recipe_update', kwargs={'object_id': item}))
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(Recipe.objects.filter(id=item).exists())
#
#         # things should be deleted cascade
#         self.assertTrue(Ingredient.objects.filter(name='Woda').exists())
#         self.assertFalse(Recipe.objects.filter(name='Lemoniada').exists())

# endregion
