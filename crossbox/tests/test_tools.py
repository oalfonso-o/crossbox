import datetime
from freezegun import freeze_time

from django.test import TestCase

from crossbox.views.reservation import get_monday_from_page


class ToolsCase(TestCase):

    @freeze_time('2019-05-14')
    def test_get_monday_from_page_on_tuesday(self):
        monday0 = get_monday_from_page(0)
        monday1 = get_monday_from_page(1)
        monday4 = get_monday_from_page(4)
        self.assertEquals(monday0, datetime.date(year=2019, month=5, day=13))
        self.assertEquals(monday1, datetime.date(year=2019, month=5, day=20))
        self.assertEquals(monday4, datetime.date(year=2019, month=6, day=10))

    @freeze_time('2019-05-17')
    def test_get_monday_from_page_on_friday(self):
        monday0 = get_monday_from_page(0)
        self.assertEquals(monday0, datetime.date(year=2019, month=5, day=13))

    @freeze_time('2019-05-18')
    def test_get_monday_from_page_on_saturday(self):
        monday0 = get_monday_from_page(0)
        self.assertEquals(monday0, datetime.date(year=2019, month=5, day=13))

    @freeze_time('2019-05-19')
    def test_get_monday_from_page_on_sunday(self):
        monday0 = get_monday_from_page(0)
        self.assertEquals(monday0, datetime.date(year=2019, month=5, day=20))
