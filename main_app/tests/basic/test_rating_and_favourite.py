from main_app.tests.TestCaseSpecialUser import *
from django.test import tag
from main_app.tests.TestSetupDatabase import *
from django.urls import reverse
import json
from accounts.models import *

@tag('recipe', 'rate', 'not_logged_user')
class AddRatingTestNotLoggedUser(TestCase):
    def setUp(self):
        TestDatabase.create_default_test_database(recipes=True)

    def test_view_correct_response_get(self):
        item = Recipe.objects.get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_rate', kwargs={'object_id': item}))
        self.assertEqual(json.loads(response.content), {'rating': None, 'mean': 0, 'favourite': False})

    def test_view_correct_response_post(self):
        item = Recipe.objects.get(name='Lemoniada').id
        data = {'rating':5, 'favourite':False}
        response = self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        self.assertEqual(json.loads(response.content), {'rating': None, 'mean': None, 'favourite':None})


@tag('recipe', 'rate', 'logged_user')
class AddRatingTestLoggedUser(TestCaseLoggedUser):
    def setUp(self):
        super().setUp()
        TestDatabase.create_database_with_two_recipes()

    def test_view_correct_response_get(self):
        item = Recipe.objects.get(name='Lemoniada').id
        response = self.client.get(reverse('recipe_rate', kwargs={'object_id': item}))
        self.assertEqual(json.loads(response.content), {'rating': None, 'mean': 0, 'favourite': False})

    def test_view_correct_response_empty_post(self):
        item = Recipe.objects.get(name='Lemoniada').id
        data = {}
        response = self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        self.assertEqual(len(Rating.objects.filter()),0)
        self.assertEqual(json.loads(response.content), {'rating': None, 'mean': None, 'favourite':None})

    def test_view_correct_response_post(self):
        item = Recipe.objects.get(name='Lemoniada').id
        data = {'rating':5, 'favourite':False}
        response = self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        self.assertEqual(json.loads(response.content), {'rating': 5, 'mean': 5, 'favourite': False})
        self.assertEqual(len(Rating.objects.filter()),1)

    def test_view_correct_response_incorrect_rating_post(self):
        item = Recipe.objects.get(name='Lemoniada').id
        data = {'rating':1.2, 'favourite':False}
        response = self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        self.assertEqual(json.loads(response.content), {'rating': None, 'mean': None, 'favourite': None})
        self.assertEqual(len(Rating.objects.filter()),0)

    def test_view_correct_response_get_after_post(self):
        item = Recipe.objects.get(name='Oranżada').id
        data = {'rating':5, 'favourite':False}
        self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        response = self.client.get(reverse('recipe_rate', kwargs={'object_id': item}))
        self.assertEqual(json.loads(response.content), {'rating': 5, 'mean': 5, 'favourite': False})

@tag('recipe', 'rate', 'logged_user', 'two')
class AddRatingTestTwoLoggedUsers(TestCase):
    def setUp(self):
        super().setUp()
        TestDatabase.create_default_test_database(recipes=True)

    def test_view_correct_response(self):
        item = Recipe.objects.get(name='Lemoniada').id
        self.client = Client()
        self.client.force_login(User.objects.get_or_create(username='c_logged')[0])
        data = {'rating':5, 'favourite':False}
        self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        self.client = Client()
        self.client.force_login(User.objects.get_or_create(username='c_logged_2')[0])
        response = self.client.get(reverse('recipe_rate', kwargs={'object_id': item}))
        self.assertEqual(json.loads(response.content), {'rating': None, 'mean': 5, 'favourite': False})
        data = {'rating':2, 'favourite':False}
        response = self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        self.assertEqual(json.loads(response.content), {'rating': 2, 'mean': 3.5, 'favourite': False})


@tag('recipe', 'rate', 'logged_user')
class AddFavouriteTestLoggedUser(TestCaseLoggedUser):
    def setUp(self):
        super().setUp()
        TestDatabase.create_default_test_database(recipes=True)

    def test_view_correct_response_get_after_post(self):
        item = Recipe.objects.get(name='Lemoniada').id
        data = {'favourite':True}
        self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        response = self.client.get(reverse('recipe_rate', kwargs={'object_id': item}))
        self.assertEqual(json.loads(response.content), {'rating': None, 'mean': 0, 'favourite': True})

    def test_view_correct_response_like_and_unlike(self):
        item = Recipe.objects.get(name='Lemoniada').id
        data = {'favourite':True}
        self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        self.client.post(reverse('recipe_rate', kwargs={'object_id': item}), data)
        response = self.client.get(reverse('recipe_rate', kwargs={'object_id': item}))
        self.assertEqual(json.loads(response.content), {'rating': None, 'mean': 0, 'favourite': False})
