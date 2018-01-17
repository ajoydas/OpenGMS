from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.test import TestCase


# models test
from authentication.models import Client


class UserTest(TestCase):

    def create_client(self, username, password):
        user = User.objects.create_user(username=username, password=password)
        user.profile.account_type = 0
        user.save()
        return user.client

    def test_client_creation(self):
        c = self.create_client("client1", "client1")
        self.assertTrue(isinstance(c, Client))