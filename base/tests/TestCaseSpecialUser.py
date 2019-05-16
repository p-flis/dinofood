from django.test import TestCase
from django.test import Client
from accounts.models import User


class TestCaseLoggedUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get_or_create(username='c_logged')[0])


class TestCaseSuperuser(TestCase):
    def setUp(self):
        password = 'password'
        my_admin = User.objects.create_superuser('sup_user', 'myemail@test.com', password)
        self.client = Client()
        self.client.login(username=my_admin.username, password=password)
