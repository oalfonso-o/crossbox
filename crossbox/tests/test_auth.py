from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.test import Client

from .tools import with_login
from crossbox.models import Subscriber


class AuthCase(TestCase):

    def tearDown(self):
        Subscriber.objects.all().delete()

    def test_login(self):
        self.assertIn('_auth_user_id', self.client.session)
        self.client_no_auth = Client()
        self.assertNotIn('_auth_user_id', self.client_no_auth.session)

    @with_login()
    def test_auth_user_calls_auth_route_ok(self):
        response = self.client.get(path=reverse('reservation'))
        self.assertEquals(response.status_code, HTTPStatus.OK)

    @with_login()
    def test_auth_user_calls_no_auth_route_redirect(self):
        response = self.client.get(path=reverse('login'))
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_no_auth_user_calls_auth_route_redirect(self):
        self.client_no_auth = Client()
        response = self.client_no_auth.get(path=reverse('reservation'))
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_no_auth_user_calls_no_auth_route_ok(self):
        self.client_no_auth = Client()
        response = self.client_no_auth.get(path=reverse('login'))
        self.assertEquals(response.status_code, HTTPStatus.OK)
