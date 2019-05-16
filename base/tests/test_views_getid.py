from django.shortcuts import render
from django.test import TestCase
from django.urls import reverse
# from django.test import Client
import json

from base.models import *


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
        response = self.client.get(reverse('ingredient_id', kwargs={'ing_id': item}))
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
