import datetime
from http import HTTPStatus
from unittest.mock import patch
from freezegun import freeze_time

from django.urls import reverse
from django.contrib.auth.models import User

from crossbox.tests.mixins import BaseTestCase
from crossbox.exceptions import LimitExceed
from crossbox.models.day import Day
from crossbox.models.hour import Hour
from crossbox.models.session import Session
from crossbox.models.reservation import Reservation
from crossbox.tests.tools import (
    with_login,
    generic_session_fields,
    create_session,
)


class ReservationsCase(BaseTestCase):

    fixtures = [
        'users', 'hours', 'days', 'capacity_limits', 'session_types', 'tracks',
        'week_templates', 'session_templates'
    ]

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_view(self):
        gen_session_flds = generic_session_fields()
        sessions_kwargs = []
        for hour in Hour.objects.all():
            for i in range(Day.objects.count()):
                sessions_kwargs.append({
                    'date': datetime.date(year=2020, month=1, day=i+1),
                    'hour': hour,
                    **gen_session_flds,
                })
        Session.objects.bulk_create([
            Session(**kwargs)
            for kwargs in sessions_kwargs
        ])
        expected_hours = [
            {'id': 1, 'hour': datetime.time(8, 0)},
            {'id': 2, 'hour': datetime.time(9, 0)},
            {'id': 3, 'hour': datetime.time(10, 0)},
            {'id': 4, 'hour': datetime.time(11, 0)},
            {'id': 5, 'hour': datetime.time(12, 0)},
            {'id': 6, 'hour': datetime.time(13, 0)},
            {'id': 7, 'hour': datetime.time(14, 0)},
            {'id': 8, 'hour': datetime.time(15, 0)},
            {'id': 9, 'hour': datetime.time(16, 0)},
            {'id': 10, 'hour': datetime.time(17, 0)},
            {'id': 11, 'hour': datetime.time(18, 0)},
            {'id': 12, 'hour': datetime.time(19, 0)},
            {'id': 13, 'hour': datetime.time(20, 0)},
            {'id': 14, 'hour': datetime.time(21, 0)},
        ]

        response = self.client.get(reverse('reservation'))
        context = response.context
        context_hours = [dict(h) for h in context['hours'].values()]

        self.assertEquals(context_hours, expected_hours)
        self.assertEquals(len(context['days']), 6)
        for sessions in context['days']:
            self.assertEquals(len(sessions), 15)
            self.assertTrue(isinstance(sessions[0], datetime.date))
            self.assertEquals(len(sessions[1].keys()), 11)
        self.assertEquals(context['wods'], 1)
        self.assertEquals(context['page'], 0)
        self.assertEquals(
            context['from_date'], datetime.date(2019, 12, 30))
        self.assertEquals(context['to_date'], datetime.date(2020, 1, 4))

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_view_return_only_current_week_sessions(self):
        create_session(date=datetime.date(year=2019, month=12, day=20))
        create_session(date=datetime.date(year=2020, month=1, day=10))
        create_session()  # default is 2020-01-02

        response = self.client.get(reverse('reservation'))

        for day, session in response.context['days']:
            if day != datetime.date(2020, 1, 2):
                self.assertFalse(session['session'])
            else:
                self.assertTrue(session['session'])

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_view_session_type(self):
        created_session = create_session()

        response = self.client.get(reverse('reservation'))
        day_rows = response.context['days'][3]
        day_sessions = day_rows[1:]  # 0 is a date for table header in frontend
        session = day_sessions[0]

        self.assertEquals(session['type'], created_session.session_type)

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_view_session_min_capacity(self):
        created_session = create_session()

        response = self.client.get(reverse('reservation'))
        day_rows = response.context['days'][3]
        day_sessions = day_rows[1:]  # 0 is a date for table header in frontend
        session = day_sessions[0]

        self.assertEquals(
            session['min_capacity'], created_session.capacity_limit.minimum)

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_view_session_max_capacity(self):
        created_session = create_session()

        response = self.client.get(reverse('reservation'))
        day_rows = response.context['days'][3]
        day_sessions = day_rows[1:]  # 0 is a date for table header in frontend
        session = day_sessions[0]

        self.assertEquals(
            session['max_capacity'], created_session.capacity_limit.maximum)

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_view_session_track(self):
        created_session = create_session()

        response = self.client.get(reverse('reservation'))
        day_rows = response.context['days'][3]
        day_sessions = day_rows[1:]  # 0 is a date for table header in frontend
        session = day_sessions[0]

        self.assertEquals(
            session['track'], created_session.track)

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_create_no_wods(self):
        session = create_session()  # default on day 2
        user = User.objects.get(pk=1)
        user.subscriber.wods = 0
        user.subscriber.save()

        self._reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='no_wods',
        )

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_create_already_reserved(self):
        session = create_session()  # default on day 2
        user = User.objects.get(pk=1)
        user.subscriber.wods = 2
        user.subscriber.save()
        # Reservate first time
        self._reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.OK,
            result_expected='created',
        )
        # Now test reservate second time on same session
        self._reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='already_reserved',
        )

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_create_max_reservations(self):
        session = create_session()  # default on day 2
        users = User.objects.bulk_create([
            User(username=f'user_{i}')
            for i in range(session.capacity_limit.maximum)
        ])
        for i in range(session.capacity_limit.maximum):
            Reservation.objects.create(session=session, user=users[i])
        self._reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='max_reservations',
        )

    @with_login()
    def test_reservation_create_session_not_found(self):
        self._reservation_view_test(
            mode='create',
            session_id=12345,
            status_code_expected=HTTPStatus.NOT_FOUND,
            result_expected='session_not_found',
        )

    @with_login()
    @freeze_time('2020-01-01 11:00:01')
    def test_reservation_create_session_started(self):
        """
        when:
        - is after the begining of the session
        then:
        - return a FORBIDDEN response with 'session_started' result
        """
        hour = Hour.objects.get(hour=datetime.time(hour=11))
        session = create_session(
            date=datetime.datetime(year=2020, month=1, day=1), hour=hour
        )
        self._reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='session_started',
        )

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_create_ok(self):
        session = create_session()  # default on day 2
        self.assertEquals(self.user.subscriber.wods, 1)
        self._reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.OK,
            result_expected='created',
        )
        self.user.subscriber.refresh_from_db()
        self.assertEquals(self.user.subscriber.wods, 0)

    @with_login()
    def test_reservation_delete_session_not_found(self):
        self._reservation_view_test(
            mode='delete',
            session_id=12345,
            status_code_expected=HTTPStatus.NOT_FOUND,
            result_expected='session_not_found',
        )

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_delete_reservation_not_found(self):
        session = create_session()
        self._reservation_view_test(
            mode='delete',
            session_id=session.pk,
            status_code_expected=HTTPStatus.NOT_FOUND,
            result_expected='no_reservation',
        )

    @with_login()
    @freeze_time('2020-01-01 00:00:00')
    @patch('django.db.models.QuerySet.count')
    def test_reservation_delete_is_too_late(self, QuerySetCountMock):
        """It's not allowed to cancel a reservation on the same day"""
        hour = Hour(hour=datetime.time(23, 59))
        hour.save()
        day = datetime.date(year=2020, month=1, day=1)
        session = create_session(date=day, hour=hour)
        QuerySetCountMock.return_value = 5
        self._reservation_view_test(
            mode='delete',
            session_id=session.pk,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='is_too_late',
        )

    @with_login()
    @freeze_time('2020-01-02 10:00:00')
    @patch('django.db.models.QuerySet.count')
    def test_reservation_delete_ok_is_too_late_but_few_people(
            self, QuerySetCountMock):
        """Refund wod if len(reservations) is less than the minimum limit
        Even when it's the same day of the session, only in that case it's
        allowed to cancel a reservation, because is considered fair to save
        that wod and check if it's possible to cancel that session because of
        not enough people
        """
        session = create_session(
            hour=Hour.objects.get(hour=datetime.time(hour=12))
        )
        QuerySetCountMock.return_value = session.capacity_limit.minimum - 1
        Reservation.objects.create(
            session=session, user=User.objects.get(pk=1))
        self._reservation_view_test(
            mode='delete',
            session_id=session.pk,
            status_code_expected=HTTPStatus.OK,
            result_expected='deleted',
        )
        self.user.subscriber.refresh_from_db()
        self.assertEquals(self.user.subscriber.wods, 2)

    @with_login()
    @freeze_time('2020-01-01 23:59:59')
    @patch('django.db.models.QuerySet.count')
    def test_reservation_delete_ok(self, QuerySetCountMock):
        session = create_session()
        reservation = Reservation(user=self.user, session=session)
        QuerySetCountMock.return_value = 1
        reservation.save()
        self._reservation_view_test(
            mode='delete',
            session_id=session.pk,
            status_code_expected=HTTPStatus.OK,
            result_expected='deleted',
        )
        self.user.subscriber.refresh_from_db()
        self.assertEquals(self.user.subscriber.wods, 2)

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_create_limit_exceed(self):
        """When trying to save a reservation on a full session, raise exception
        """
        session = create_session()  # default on day 2
        for i in range(session.capacity_limit.maximum):
            user = User(username=f'user_{i}')
            user.save()
            Reservation.objects.create(session=session, user=user)
        with self.assertRaises(LimitExceed):
            Reservation.objects.create(session=session, user=user)

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
    @freeze_time('2020-01-01')
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
    def _reservation_view_test(
            self, mode, session_id, status_code_expected, result_expected):
        response = self.client.post(
            path=reverse(f'reservation-{mode}'),
            data={'session': session_id},
            content_type='application/json',
        )
        self.assertEquals(response.status_code, status_code_expected)
        self.assertEquals(response.json()['result'], result_expected)
