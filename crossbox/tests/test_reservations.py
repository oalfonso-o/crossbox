import datetime
from http import HTTPStatus
from unittest.mock import patch
from freezegun import freeze_time

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .tools import with_login
from .constants import EXPECTED_RESERVATION_DAYS
from crossbox.models.session import Session
from crossbox.models.hour import Hour
from crossbox.models.reservation import Reservation
from crossbox.constants import MAX_RESERVATION_PLACES


class ReservationsCase(TestCase):

    fixtures = [
        'users', 'hours', 'days', 'capacity_limits', 'session_types', 'tracks',
        'week_templates', 'session_templates', 'subscribers'
    ]

    @with_login()
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

    @with_login()
    @freeze_time('2018-12-31')
    def test_reservation_create_no_wods(self):
        # New users have always 1 initial free wod, let's spend it
        self.reservation_view_test(
            mode='create',
            session_id=2,
            status_code_expected=HTTPStatus.OK,
            result_expected='created',
        )
        # Now test no_wod functionality
        self.reservation_view_test(
            mode='create',
            session_id=3,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='no_wods',
        )

    @with_login()
    @freeze_time('2018-12-31')
    def test_reservation_create_already_reserved(self):
        # Reservate first time
        self.reservation_view_test(
            mode='create',
            session_id=2,
            status_code_expected=HTTPStatus.OK,
            result_expected='created',
        )
        # Now test reservate second time on same session
        self.user.subscriber.wods += 1
        self.user.subscriber.save()
        self.reservation_view_test(
            mode='create',
            session_id=2,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='already_reserved',
        )

    @with_login()
    @freeze_time('2018-12-31')
    def test_reservation_create_max_reservations(self):
        session = Session.objects.get(pk=2)
        users = User.objects.bulk_create([
            User(username=f'user_{i}')
            for i in range(MAX_RESERVATION_PLACES)
        ])
        for i in range(MAX_RESERVATION_PLACES):
            Reservation.objects.create(session=session, user=users[i])
        self.reservation_view_test(
            mode='create',
            session_id=2,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='max_reservations',
        )

    @with_login()
    def test_reservation_create_session_not_found(self):
        self.reservation_view_test(
            mode='create',
            session_id=12345,
            status_code_expected=HTTPStatus.NOT_FOUND,
            result_expected='session_not_found',
        )

    @with_login()
    @freeze_time('2019-12-31 11:00:01')
    def test_reservation_create_session_started(self):
        """
        when:
        - now is after the begining of the session
        then:
        - returns a FORBIDDEN response with 'session_started' result
        """
        self.reservation_view_test(
            mode='create',
            session_id=2,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='session_started',
        )

    @with_login()
    @freeze_time('2018-12-31')
    def test_reservation_create_ok(self):
        self.assertEquals(self.user.subscriber.wods, 1)
        self.reservation_view_test(
            mode='create',
            session_id=2,
            status_code_expected=HTTPStatus.OK,
            result_expected='created',
        )
        self.user.subscriber.refresh_from_db()
        self.assertEquals(self.user.subscriber.wods, 0)

    @with_login()
    def reservation_view_test(
            self, mode, session_id, status_code_expected, result_expected):
        response = self.client.post(
            path=reverse(f'reservation-{mode}'),
            data={'session': session_id},
            content_type='application/json',
        )
        self.assertEquals(response.status_code, status_code_expected)
        self.assertEquals(response.json()['result'], result_expected)

    @with_login()
    def test_reservation_delete_session_not_found(self):
        self.reservation_view_test(
            mode='delete',
            session_id=12345,
            status_code_expected=HTTPStatus.NOT_FOUND,
            result_expected='session_not_found',
        )

    @with_login()
    @freeze_time('2018-12-31 8:00:00')
    def test_reservation_delete_no_subscriber(self):
        """
        given:
        - a request to delete a reservation arrives
        when:
        - user has no subscriber, so can't refund the wod
        then:
        - returns a FORBIDDEN response with 'no_subscriber' result
        """
        pass  # TODO

    @with_login()
    @freeze_time('2018-12-30 10:00:00')
    def test_reservation_delete_reservation_not_found(self):
        self.reservation_view_test(
            mode='delete',
            session_id=2,
            status_code_expected=HTTPStatus.NOT_FOUND,
            result_expected='no_reservation',
        )

    @with_login()
    def test_reservation_delete_unhandled_error(self):
        """
        given:
        - a request to delete a reservation arrives
        when:
        - any other kind of error happened
        then:
        - returns a FORBIDDEN response with 'unhandled' result
        """
        pass  # TODO

    @with_login()
    @freeze_time('2019-01-01 00:00:00')
    @patch('django.db.models.QuerySet.count')
    def test_reservation_delete_is_too_late(self, QuerySetCountMock):
        hour = Hour(hour=datetime.time(23, 59))
        hour.save()
        day = datetime.date(year=2019, month=1, day=1)
        session = Session(date=day, hour=hour)
        session.save()
        QuerySetCountMock.return_value = 5
        self.reservation_view_test(
            mode='delete',
            session_id=session.id,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='is_too_late',
        )

    @with_login()
    @freeze_time('2019-01-02 00:00:00')
    @patch('django.db.models.QuerySet.count')
    def test_reservation_delete_ok_is_too_late_but_few_people(
            self, QuerySetCountMock):
        # session 21 -> day: 2019-01-02, hour: 17:00:00
        QuerySetCountMock.return_value = 2
        self.reservation_view_test(
            mode='delete',
            session_id=21,
            status_code_expected=HTTPStatus.OK,
            result_expected='deleted',
        )
        self.user.subscriber.refresh_from_db()
        self.assertEquals(self.user.subscriber.wods, 2)

    @with_login()
    @freeze_time('2019-01-01 23:59:59')
    @patch('django.db.models.QuerySet.count')
    def test_reservation_delete_ok(self, QuerySetCountMock):
        hour = Hour(hour=datetime.time(0, 0))
        hour.save()
        day = datetime.date(year=2019, month=1, day=2)
        session = Session(date=day, hour=hour)
        session.save()
        reservation = Reservation(user=self.user, session=session)
        QuerySetCountMock.return_value = 1
        reservation.save()
        QuerySetCountMock.return_value = 14
        self.reservation_view_test(
            mode='delete',
            session_id=session.id,
            status_code_expected=HTTPStatus.OK,
            result_expected='deleted',
        )
        self.user.subscriber.refresh_from_db()
        self.assertEquals(self.user.subscriber.wods, 2)
