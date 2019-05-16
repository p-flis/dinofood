from django.urls import reverse
from main_app.tests.TestCaseSpecialUser import *

from main_app.models import *


class DeleteCategoryViewTestSuperuser(TestCaseSuperuser):
    @classmethod
    def setUpTestData(cls):
        category_names = [
            "Liquids",
            "Fruits"
        ]
        ingredient_data = [
            ("Water", 2, "Liquids"),
            ("Lemon", 8, "Fruits")

        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1], category=Category.objects.get(name=n[2]))
                                        for n in ingredient_data])
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/category/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Category.objects.only('id').get(name='Liquids').id
        response = self.client.get('/category/{}/delete'.format(item))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        item = Category.objects.only('id').get(name='Liquids').id
        response = self.client.get(reverse('category_delete', kwargs={'cat_id': item}))
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_properly(self):
        item = Category.objects.only('id').get(name='Liquids').id
        response = self.client.get(reverse('category_delete', kwargs={'cat_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertFalse(Category.objects.filter(name='Liquids').exists())
        self.assertFalse(Ingredient.objects.filter(name='Water').exists())
        self.assertFalse(Dish.objects.filter(name='Lemonade').exists())


class DeleteCategoryViewTestNotSuperuser(TestCase):
    @classmethod
    def setUpTestData(cls):
        category_names = [
            "Liquids",
            "Fruits"
        ]
        ingredient_data = [
            ("Water", 2, "Liquids"),
            ("Lemon", 8, "Fruits")

        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1], category=Category.objects.get(name=n[2]))
                                        for n in ingredient_data])
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    def test_view_correct_redirection(self):
        item = Category.objects.only('id').get(name='Liquids').id
        response = self.client.get('/category/{}/delete'.format(item), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('category_delete',
                                                                                kwargs={'cat_id': item}),
                             status_code=302,
                             target_status_code=200)

    def test_view_correct_redirection_id_doesnt_exist(self):
        response = self.client.get('/category/999/delete', follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('category_delete', kwargs={'cat_id': 999}),
                             status_code=302,
                             target_status_code=200)


class DeleteRecipeViewTestSuperuser(TestCaseSuperuser):
    @classmethod
    def setUpTestData(cls):
        category_names = [
            "Liquids",
            "Fruits"
        ]
        ingredient_data = [
            ("Water", 2, "Liquids"),
            ("Lemon", 8, "Fruits")

        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1], category=Category.objects.get(name=n[2]))
                                        for n in ingredient_data])
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/recipe/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Dish.objects.only('id').get(name='Lemonade').id
        response = self.client.get('/recipe/{}/delete'.format(item))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        item = Dish.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'dish_id': item}))
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_properly(self):
        item = Dish.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'dish_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertTrue(Category.objects.filter(name='Liquids').exists())
        self.assertTrue(Ingredient.objects.filter(name='Water').exists())
        self.assertFalse(Dish.objects.filter(name='Lemonade').exists())

    def test_view_redirects_properly(self):
        item = Dish.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'dish_id': item}), follow=True)
        self.assertRedirects(response, reverse('recipe'))


class DeleteRecipeViewTestNotSuperuser(TestCaseLoggedUser):
    @classmethod
    def setUpTestData(cls):
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

    def test_view_adds_and_deletes_recipe_owner(self):
        ingredients_list = ['Water', 'Lemon']
        quantities_list = ['1', '1']
        response = self.client.post('/recipe/new', {'name': 'Lemonade',
                                                    'description': 'water, but sour',
                                                    'recipe': '',
                                                    'ingredients': ingredients_list,
                                                    'quantities': quantities_list})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())

        item = Dish.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'dish_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertFalse(Dish.objects.filter(name='Lemonade').exists())

    def test_view_deletes_recipe_not_logged_in(self):
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

        client = Client()
        item = Dish.objects.only('id').get(name='Lemonade').id
        response = client.get(reverse('recipe_delete', kwargs={'dish_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'dish_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())

    def test_view_deletes_recipe_not_logged_in_id_doesnt_exist(self):
        client = Client()
        response = client.get(reverse('recipe_delete', kwargs={'dish_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'dish_id': 999}),
                             status_code=302,
                             target_status_code=200)

    def test_view_deletes_recipe_logged_in_not_owner(self):
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

        item = Dish.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_delete', kwargs={'dish_id': item}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'dish_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())

    def test_view_deletes_recipe_logged_in_not_owner_id_doesnt_exist(self):
        response = self.client.get(reverse('recipe_delete', kwargs={'dish_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('login') + "?next=" + reverse('recipe_delete', kwargs={'dish_id': 999}),
                             status_code=302,
                             target_status_code=200)


class DeleteIngredientViewTestSuperuser(TestCaseSuperuser):
    @classmethod
    def setUpTestData(cls):
        category_names = [
            "Liquids",
            "Fruits"
        ]
        ingredient_data = [
            ("Water", 2, "Liquids"),
            ("Lemon", 8, "Fruits")

        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1], category=Category.objects.get(name=n[2]))
                                        for n in ingredient_data])
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get('/ingredient/{}/delete'.format(item))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'ing_id': item}))
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_properly(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'ing_id': item}))
        self.assertEqual(response.status_code, 302)
        # things should be deleted cascade
        self.assertTrue(Category.objects.filter(name='Liquids').exists())
        self.assertFalse(Ingredient.objects.filter(name='Water').exists())
        self.assertFalse(Dish.objects.filter(name='Lemonade').exists())

    def test_view_redirects_properly(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'ing_id': item}), follow=True)
        self.assertRedirects(response, reverse('ingredient'))


class DeleteIngredientViewTestNotSuperuser(TestCaseLoggedUser):
    @classmethod
    def setUpTestData(cls):
        category_names = [
            "Liquids",
            "Fruits"
        ]
        ingredient_data = [
            ("Water", 2, "Liquids"),
            ("Lemon", 8, "Fruits")

        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1], category=Category.objects.get(name=n[2]))
                                        for n in ingredient_data])
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    def test_view_deletes_ingredient_not_logged_in(self):
        client = Client()
        item = Ingredient.objects.only('id').get(name='Water').id
        response = client.get(reverse('ingredient_delete', kwargs={'ing_id': item}),follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete', kwargs={'ing_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Category.objects.filter(name='Liquids').exists())
        self.assertTrue(Ingredient.objects.filter(name='Water').exists())
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())

    def test_view_deletes_ingredient_not_logged_in_id_doesnt_exist(self):
        client = Client()
        response = client.get(reverse('ingredient_delete', kwargs={'ing_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete', kwargs={'ing_id': 999}),
                             status_code=302,
                             target_status_code=200)

    def test_view_deletes_ingredient_logged_in(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_delete', kwargs={'ing_id': item}),follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete', kwargs={'ing_id': item}),
                             status_code=302,
                             target_status_code=200)
        self.assertTrue(Category.objects.filter(name='Liquids').exists())
        self.assertTrue(Ingredient.objects.filter(name='Water').exists())
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())

    def test_view_deletes_ingredient_logged_in_id_doesnt_exist(self):
        response = self.client.get(reverse('ingredient_delete', kwargs={'ing_id': 999}), follow=True)
        self.assertRedirects(response,
                             reverse('superuser_required') + "?next=" + reverse('ingredient_delete', kwargs={'ing_id': 999}),
                             status_code=302,
                             target_status_code=200)
