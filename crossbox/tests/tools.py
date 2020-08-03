import datetime

from django.urls import reverse
from django.contrib.auth.models import User

from crossbox.models.hour import Hour
from crossbox.models.track import Track
from crossbox.models.session import Session
from crossbox.models.session_type import SessionType
from crossbox.models.capacity_limit import CapacityLimit


def with_login(username='admin'):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            self.user, _ = User.objects.get_or_create(username=username)
            self.client.post(
                reverse('login'),
                {'username': username, 'password': 'admin'}
            )
            func(self, *args, **kwargs)
        return wrapper
    return decorator


def generic_session_fields():
    return {
        'session_type': SessionType.objects.get(pk=1),
        'capacity_limit': CapacityLimit.objects.get(pk=1),
        'track': Track.objects.get(pk=1),
    }


def create_session(
    date=datetime.date(year=2020, month=1, day=2),
    hour=Hour.objects.get(pk=1),
):
    session = Session(
        date=date,
        hour=hour,
        **generic_session_fields(),
    )
    session.save()
    return session
