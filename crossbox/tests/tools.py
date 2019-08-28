from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User


def with_login(username='admin'):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            self.client = Client()
            self.user, _ = User.objects.get_or_create(username=username)
            self.client.post(
                reverse('login'),
                {'username': username, 'password': 'admin'}
            )
            func(self, *args, **kwargs)
        return wrapper
    return decorator
