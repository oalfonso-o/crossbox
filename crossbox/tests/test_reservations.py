import datetime
from http import HTTPStatus
from unittest.mock import patch
from freezegun import freeze_time

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from crossbox.models.day import Day
from crossbox.models.hour import Hour
from crossbox.models.session import Session
from crossbox.models.reservation import Reservation
from crossbox.tests.tools import (
    with_login,
    generic_session_fields,
    create_session,
)


class ReservationsCase(TestCase):

    fixtures = [
        'users', 'hours', 'days', 'capacity_limits', 'session_types', 'tracks',
        'week_templates', 'session_templates', 'subscribers'
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
        self.assertEquals(context['wods'], 50)
        self.assertEquals(context['page'], 0)
        self.assertEquals(
            context['from_date'], datetime.date(2019, 12, 30))
        self.assertEquals(context['to_date'], datetime.date(2020, 1, 4))

    @with_login()
    @freeze_time('2018-12-31')
    def test_reservation_create_no_wods(self):
        user = User.objects.get(pk=1)
        user.subscriber.wods = 0
        user.subscriber.save()

        self.reservation_view_test(
            mode='create',
            session_id=3,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='no_wods',
        )

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_create_already_reserved(self):
        session = create_session()
        # Reservate first time
        self.reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.OK,
            result_expected='created',
        )
        # Now test reservate second time on same session
        self.reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='already_reserved',
        )

    @with_login()
    @freeze_time('2020-01-01')
    def test_reservation_create_max_reservations(self):
        gen_session_flds = generic_session_fields()
        session = Session(
            date=datetime.date(year=2020, month=1, day=2),
            hour=Hour.objects.get(pk=1),
            **gen_session_flds,
        )
        session.save()
        users = User.objects.bulk_create([
            User(username=f'user_{i}')
            for i in range(gen_session_flds['capacity_limit'].maximum)
        ])
        for i in range(gen_session_flds['capacity_limit'].maximum):
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
        self.reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.FORBIDDEN,
            result_expected='session_started',
        )

    @with_login()
    @freeze_time('2018-12-31')
    def test_reservation_create_ok(self):
        session = create_session()
        self.assertEquals(self.user.subscriber.wods, 50)
        self.reservation_view_test(
            mode='create',
            session_id=session.pk,
            status_code_expected=HTTPStatus.OK,
            result_expected='created',
        )
        self.user.subscriber.refresh_from_db()
        self.assertEquals(self.user.subscriber.wods, 49)

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
        session = Session(date=day, hour=hour, **generic_session_fields())
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
        session = Session(date=day, hour=hour, **generic_session_fields())
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
