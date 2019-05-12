from django.shortcuts import render
from django.test import TestCase
from django.urls import reverse
from django.test import Client
import json

from base.models import *


class RecipeSearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category_names = [
            "Liquids",
            "Fruits"
        ]
        ingredient_data = [
            ("Water", 2, "Liquids"),
            ("Lemon", 8, "Fruits"),
            ("Apple", 5, "Fruits")

        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1], category=Category.objects.get(name=n[2]))
                                        for n in ingredient_data])
        dish_data = [
            ("Lemonade",
             "water, but sour",
             ["Water", "Lemon"]),
            ("Apple juice",
             "water, but tastes like apple",
             ["Water", "Apple"]),
        ]
        for n in dish_data:
            d = Dish(name=n[0], description=n[1])
            d.save()
            for ing_name in n[2]:
                d.ingredients.add(Ingredient.objects.get(name=ing_name), through_defaults={'quantity': 1})

    def test_view_url_exists_at_desired_location_id_exists(self):
        response = self.client.get('/recipe/search')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_get(self):
        response = self.client.get('/recipe/search')
        self.assertTemplateUsed(response, 'food/search_recipe.html')

    def test_view_uses_correct_template_post(self):
        ingredients_list = []
        ingredients_list.append('Water')
        response = self.client.post('/recipe/search', {"ingredients": ingredients_list})
        self.assertTemplateUsed(response, 'food/recipe.html')

    def test_view_finds_single_dish(self):
        ingredients_list = []
        ingredients_list.append('Water')
        ingredients_list.append('Lemon')
        response = self.client.post('/recipe/search', {"ingredients": ingredients_list})
        self.assertEqual(response.context['itemlist'].count(), 1)
        self.assertEqual(response.context['itemlist'][0].name, 'Lemonade')

    def test_view_finds_two_dishes(self):
        ingredients_list = []
        ingredients_list.append('Water')
        response = self.client.post('/recipe/search', {"ingredients": ingredients_list})
        self.assertEqual(response.context['itemlist'].count(), 2)


#region DeleteViews

class DeleteCategoryViewTest(TestCase):
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
        #things should be deleted cascade
        self.assertFalse(Category.objects.filter(name='Liquids').exists())
        self.assertFalse(Ingredient.objects.filter(name='Water').exists())
        self.assertFalse(Dish.objects.filter(name='Lemonade').exists())

class DeleteRecipeViewTest(TestCase):
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
        #things should be deleted cascade
        self.assertTrue(Category.objects.filter(name='Liquids').exists())
        self.assertTrue(Ingredient.objects.filter(name='Water').exists())
        self.assertFalse(Dish.objects.filter(name='Lemonade').exists())

class DeleteIngredientViewTest(TestCase):
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
        #things should be deleted cascade
        self.assertTrue(Category.objects.filter(name='Liquids').exists())
        self.assertFalse(Ingredient.objects.filter(name='Water').exists())
        self.assertFalse(Dish.objects.filter(name='Lemonade').exists())

#endregion

#region GetIDViews

class IngredientIDViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category_names = [
            "Liquids",
        ]
        ingredient_data = [
            ("Water", 2, "Liquids"),
        ]
        Category.objects.bulk_create([Category(name=n) for n in category_names])
        Ingredient.objects.bulk_create([Ingredient(name=n[0], price=n[1], category=Category.objects.get(name=n[2]))
                                        for n in ingredient_data])

    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/ingredient/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        response = self.client.get('/ingredient/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_id', kwargs={'ing_id':item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = Ingredient.objects.only('id').get(name='Water').id
        response = self.client.get(reverse('ingredient_id', kwargs={'ing_id': item}))
        self.assertTemplateUsed(response, 'food/ingredient_id_get.html')

class CategoryIDViewTest(TestCase):
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
    def test_view_url_exists_at_desired_location_id_doesnt_exists(self):
        response = self.client.get('/category/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        response = self.client.get('/category/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Category.objects.only('id').get(name='Liquids').id
        response = self.client.get(reverse('category_id', kwargs={'cat_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = Category.objects.only('id').get(name='Liquids').id
        response = self.client.get(reverse('category_id', kwargs={'cat_id': item}))
        self.assertTemplateUsed(response, 'food/category_id_get.html')

class RecipeIDViewTest(TestCase):
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
        response = self.client.get('/recipe/999')
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location_id_exists(self):
        item = Dish.objects.only('id').get(name='Lemonade').id
        response = self.client.get('/recipe/{}'.format(item))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        item = Dish.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_id', kwargs={'dish_id': item}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        item = Dish.objects.only('id').get(name='Lemonade').id
        response = self.client.get(reverse('recipe_id', kwargs={'dish_id': item}))
        self.assertTemplateUsed(response, 'food/recipe_id_get.html')

#endregion

#region AddViews

class AddRecipeViewTest(TestCase):

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
        ingredients_list = []
        ingredients_list.append('Water')
        ingredients_list.append('Lemon')
        quantities_list = []
        quantities_list.append('1')
        quantities_list.append('1')
        response = self.client.post('/recipe/new', {'name':'Lemonade',
                                                    'description':'water, but sour',
                                                    'ingredients':ingredients_list,
                                                    'quantities':quantities_list})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name='Lemonade').exists())
        self.assertEqual(response.url, '/recipe')

class AddIngredientViewTest(TestCase):

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
        response = self.client.post('/ingredient/new', {'name':'water', 'price':'2', 'categories':'Liquids'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name='water').exists())
        self.assertEqual(response.url, '/ingredient')


class AddCategoryViewTest(TestCase):

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

#endregion

#region DatabaseTests

def empty_database():
    Category.objects.all().delete()
    # User.objects.all().delete() #idk where it is and if it is safe to remove users

    # two of above should be enough if relations were configured properly
    # but now it is safer to delete everything
    Ingredient.objects.all().delete()
    Dish.objects.all().delete()
    DishDetails.objects.all().delete()
    Rating.objects.all().delete()


def load_db_from_json(file_name):
    with open(file_name, encoding='utf-8') as file:
        db = json.load(file)
        categories_data = db['categories']
        Category.objects.bulk_create([Category(name=category_data['name']) for category_data in categories_data])

        ingredients_data = db['ingredients']
        Ingredient.objects.bulk_create([Ingredient(name=ingredient_data['name'],
                                                   price=ingredient_data['price'],
                                                   category=Category.objects.get(name=ingredient_data['category_name']))
                                        for ingredient_data in ingredients_data])

        recipes_data = db['recipes']
        for recipe_data in recipes_data:
            d = Dish(name=recipe_data['name'], description=recipe_data['description'], recipe=recipe_data['recipe'])
            d.save()
            for ingredient_data in recipe_data['ingredients']:
                d.ingredients.add(Ingredient.objects.get(name=ingredient_data['name']),
                                  through_defaults={'quantity': ingredient_data['quantity']})


def test_empty_database(request):
    empty_database()
    return render(request, "empty_database.html")


def test_default_database(request):
    empty_database()

    load_db_from_json("default_db.json")

    return render(request, "default_database.html")

#endregion



