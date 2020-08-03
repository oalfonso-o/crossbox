import datetime
from freezegun import freeze_time
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .tools import with_login
from crossbox.models.session import Session
from crossbox.models.hour import Hour
from crossbox.admin.session import SessionAdmin, SessionAdminFilter


class SessionsCase(TestCase):

    fixtures = [
        'users', 'hours', 'days', 'capacity_limits', 'session_types', 'tracks',
        'week_templates', 'session_templates'
    ]

    @with_login()
    def test_change_session_type(self):
        hour = Hour(hour=datetime.time(0, 0))
        hour.save()
        day = datetime.date(year=2019, month=1, day=1)
        session = Session(date=day, hour=hour)
        session.save()
        self._session_view_test(
            session_id=session.id,
            status_code_expected=HTTPStatus.OK,
            result_expected='OPEN',
        )
        self._session_view_test(
            session_id=session.id,
            status_code_expected=HTTPStatus.OK,
            result_expected='ESTIRAMIENTOS',
        )
        self._session_view_test(
            session_id=session.id,
            status_code_expected=HTTPStatus.OK,
            result_expected='WOD',
        )
        self._session_view_test(
            session_id=session.id,
            status_code_expected=HTTPStatus.OK,
            result_expected='OPEN',
        )

    @with_login()
    @freeze_time('2020-01-1')
    def test_session_template_context_data_weeks(self):
        response = self.client.get(path=reverse('session-template'))
        weeks = response.context_data['weeks']
        self.assertEqual(len(weeks), 52)
        self.assertEqual(weeks[0], 'Lunes 30/12/2019 - Semana 1 (actual)')
        self.assertEqual(weeks[51], 'Lunes 21/12/2020 - Semana 52')

    @with_login()
    def test_change_session_type_no_session(self):
        response = self.client.put(
            path=reverse('change_session_type', args=[13371337]))
        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)

    def _session_view_test(
            self, session_id, status_code_expected, result_expected):
        response = self.client.put(
            path=reverse('change_session_type', args=[session_id]))
        self.assertEquals(response.status_code, status_code_expected)
        self.assertEquals(response.json()['session_type'], result_expected)


class SessionAdminFilterCase(TestCase):

    @freeze_time('2019-02-1')
    def test_queryset_depending_on_filter_selected(self):
        hour = Hour(hour=datetime.time(0, 0))
        hour.save()
        day_jan = datetime.date(year=2019, month=1, day=1)
        day_feb = datetime.date(year=2019, month=2, day=1)
        day_mar = datetime.date(year=2019, month=3, day=1)
        Session.objects.bulk_create([
            Session(date=day_jan, hour=hour),
            Session(date=day_feb, hour=hour),
            Session(date=day_mar, hour=hour),
        ])
        session_filter = SessionAdminFilter(None, {}, Session, SessionAdmin)
        session_filter.used_parameters['filter'] = None
        from_this_week_sessions = session_filter.queryset(
            None, Session.objects.all())
        self.assertEquals(from_this_week_sessions[0].date, day_feb)
        self.assertEquals(from_this_week_sessions[1].date, day_mar)
        self.assertEquals(from_this_week_sessions.count(), 2)

        session_filter.used_parameters['filter'] = 'past'
        past_sessions = session_filter.queryset(None, Session.objects.all())
        self.assertEquals(past_sessions[0].date, day_jan)
        self.assertEquals(past_sessions.count(), 1)

        session_filter.used_parameters['filter'] = 'all_desc'
        all_desc_sessions = session_filter.queryset(
            None, Session.objects.all())
        self.assertEquals(all_desc_sessions[0].date, day_mar)
        self.assertEquals(all_desc_sessions[1].date, day_feb)
        self.assertEquals(all_desc_sessions[2].date, day_jan)

        session_filter.used_parameters['filter'] = 'all_asc'
        all_asc_sessions = session_filter.queryset(None, Session.objects.all())
        self.assertEquals(all_asc_sessions[0].date, day_jan)
        self.assertEquals(all_asc_sessions[1].date, day_feb)
        self.assertEquals(all_asc_sessions[2].date, day_mar)
