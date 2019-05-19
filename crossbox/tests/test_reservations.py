import datetime
from freezegun import freeze_time
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User

from .data import EXPECTED_RESERVATION_DAYS


class ReservationsCase(TestCase):

    fixtures = ['tests_auth', 'tests_base']

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')
        self.user_id = next(iter(self.client.session.items()))[1]
        self.user = User.objects.get(id=self.user_id)

    def test_login(self):
        self.assertIn('_auth_user_id', self.client.session)

    @freeze_time('2019-05-14')
    def test_reservation_view(self):
        response = self.client.get(reverse('reservation'))
        context = response.context
        expected_hours = [
            {'id': 3, 'hour': datetime.time(10, 0)},
            {'id': 4, 'hour': datetime.time(11, 0)},
            {'id': 5, 'hour': datetime.time(12, 0)},
            {'id': 6, 'hour': datetime.time(13, 0)},
            {'id': 10, 'hour': datetime.time(17, 0)},
            {'id': 11, 'hour': datetime.time(18, 0)},
            {'id': 12, 'hour': datetime.time(19, 0)},
            {'id': 13, 'hour': datetime.time(20, 0)}
        ]
        context_hours = [dict(h) for h in context['hours'].values()]
        self.assertEquals(context_hours, expected_hours)
        self.assertEquals(context['days'], EXPECTED_RESERVATION_DAYS)
        self.assertEquals(context['wods'], 1)
        self.assertEquals(context['page'], 0)

    def test_reservation_create_no_wods(self):
        """
        given:
        - a request to create a reservation arrives
        when:
        - that user's subscriber has no wods left
        then:
        - returns a FORBIDDEN response with 'no_wods' result
        """
        # New users have always 1 initial free wod, let's spend it
        self.reservation_create_test(
            session_id=2,
            status_code_expected=HTTPStatus.OK,
            result_expected='created',
        )
        # Now test no_wod functionality
        self.reservation_create_test(
            session_id=3,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='no_wods',
        )

    def test_reservation_create_already_reserved(self):
        """
        given:
        - a request to create a reservation arrives
        when:
        - that user's subscriber has already reserved in that session
        then:
        - returns a FORBIDDEN response with 'already_reserved' result
        """
        # Reservate first time
        self.reservation_create_test(
            session_id=2,
            status_code_expected=HTTPStatus.OK,
            result_expected='created',
        )
        # Now test reservate second time on same session
        self.user.subscriber.wods += 1
        self.user.subscriber.save()
        self.reservation_create_test(
            session_id=2,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='already_reserved',
        )

    def reservation_create_test(
            self, session_id, status_code_expected, result_expected):
        response = self.client.post(
            path=reverse('reservation-create'),
            data={'session': session_id},
            content_type='application/json',
        )
        self.assertEquals(response.status_code, status_code_expected)
        self.assertEquals(response.json()['result'], result_expected)
