import datetime
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .tools import with_login
from crossbox.models import Hour, Session


class SessionsCase(TestCase):

    fixtures = ['tests_base']

    @with_login()
    def test_change_session_type(self):
        hour = Hour(hour=datetime.time(0, 0))
        hour.save()
        day = datetime.date(year=2019, month=1, day=1)
        session = Session(date=day, hour=hour)
        session.save()
        self.session_view_test(
            session_id=session.id,
            status_code_expected=HTTPStatus.OK,
            result_expected='OPEN',
        )
        self.session_view_test(
            session_id=session.id,
            status_code_expected=HTTPStatus.OK,
            result_expected='ESTIRAMIENTOS',
        )
        self.session_view_test(
            session_id=session.id,
            status_code_expected=HTTPStatus.OK,
            result_expected='WOD',
        )
        self.session_view_test(
            session_id=session.id,
            status_code_expected=HTTPStatus.OK,
            result_expected='OPEN',
        )

    @with_login()
    def test_change_session_type_no_session(self):
        response = self.client.put(
            path=reverse('change_session_type', args=[13371337]))
        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)

    @with_login()
    def session_view_test(
            self, session_id, status_code_expected, result_expected):
        response = self.client.put(
            path=reverse('change_session_type', args=[session_id]))
        self.assertEquals(response.status_code, status_code_expected)
        self.assertEquals(response.json()['session_type'], result_expected)
