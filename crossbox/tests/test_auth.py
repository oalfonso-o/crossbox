from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from .tools import with_login


class AuthCase(TestCase):

    fixtures = [
        'users', 'hours', 'days', 'capacity_limits', 'session_types', 'tracks',
        'week_templates', 'session_templates'
    ]

    @with_login()
    def test_auth_user_calls_auth_route_ok(self):
        """ Middleware will be quite and let django resolve the url """
        response = self.client.get(reverse('reservation'))
        self.assertEquals(response.status_code, HTTPStatus.OK)

    @with_login()
    def test_auth_user_calls_no_auth_route_redirect(self):
        for no_auth_route in settings.NOT_LOGIN_REQUIRED_ROUTES:
            path = (
                reverse(no_auth_route)
                if no_auth_route != 'password_reset_confirm'
                else reverse(no_auth_route, args=['a', 'b'])
            )
            response = self.client.get(path)
            self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_no_auth_user_calls_auth_route_redirect(self):
        response = self.client.get(path=reverse('reservation'))
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_no_auth_user_calls_no_auth_route_ok(self):
        response = self.client.get(path=reverse('login'))
        self.assertEquals(response.status_code, HTTPStatus.OK)
