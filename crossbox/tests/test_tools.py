import datetime
from freezegun import freeze_time

from django.test import TestCase

from crossbox.models import Session, Hour
from crossbox.views.reservation import get_monday_from_page


class ToolsCase(TestCase):

    @freeze_time('2019-05-14')
    def test_get_monday_from_page_tuesday(self):
        monday0 = get_monday_from_page(0)
        monday1 = get_monday_from_page(1)
        monday4 = get_monday_from_page(4)
        self.assertEquals(monday0, datetime.date(year=2019, month=5, day=13))
        self.assertEquals(monday1, datetime.date(year=2019, month=5, day=20))
        self.assertEquals(monday4, datetime.date(year=2019, month=6, day=10))

    @freeze_time('2019-05-17 23:59:59')
    def test_get_monday_from_page_friday(self):
        monday = get_monday_from_page(0)
        self.assertEquals(monday, datetime.date(year=2019, month=5, day=13))

    @freeze_time('2019-05-18 13:00:00')
    def test_get_monday_from_page_saturday_no_more_session_at_13(self):
        monday = get_monday_from_page(0)
        self.assertEquals(monday, datetime.date(year=2019, month=5, day=13))

    @freeze_time('2019-05-18 14:00:00')
    def test_get_monday_from_page_saturday_no_more_session_at_14(self):
        monday = get_monday_from_page(0)
        self.assertEquals(monday, datetime.date(year=2019, month=5, day=13))

    @freeze_time('2019-05-18 14:00:01')
    def test_get_monday_from_page_saturday_no_more_session_after_14(self):
        monday = get_monday_from_page(0)
        self.assertEquals(monday, datetime.date(year=2019, month=5, day=20))

    @freeze_time('2019-05-18 10:00:00')
    def test_get_monday_from_page_saturday_before_last_session(self):
        self._create_saturday_session()
        monday = get_monday_from_page(0)
        self.assertEquals(monday, datetime.date(year=2019, month=5, day=13))

    @freeze_time('2019-05-18 11:00:00')
    def test_get_monday_from_page_saturday_before_last_session_limit(self):
        self._create_saturday_session()
        monday = get_monday_from_page(0)
        self.assertEquals(monday, datetime.date(year=2019, month=5, day=13))

    @freeze_time('2019-05-18 11:00:01')
    def test_get_monday_from_page_saturday_after_last_session(self):
        self._create_saturday_session()
        monday = get_monday_from_page(0)
        self.assertEquals(monday, datetime.date(year=2019, month=5, day=20))

    @freeze_time('2019-05-19 00:00:00')
    def test_get_monday_from_page_sunday(self):
        monday = get_monday_from_page(0)
        self.assertEquals(monday, datetime.date(year=2019, month=5, day=20))

    @staticmethod
    def _create_saturday_session():
        hour = Hour(hour=datetime.time(10))
        hour.save()
        day = datetime.date(year=2019, month=5, day=18)  # Saturday
        Session.objects.create(date=day, hour=hour)
