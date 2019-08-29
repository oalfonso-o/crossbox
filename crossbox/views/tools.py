from datetime import date, timedelta, datetime

from crossbox.models import Session
from crossbox.constants import (
    WEEK_DAYS,
    SATURDAY_TIMEDELTA_DAYS,
    DEFAULT_LAST_SESSION_HOUR,
)


def active_page_number(request):
    first_page = 0
    return int(request.GET.get('page', first_page) or first_page)


def get_monday_from_page(page_number):
    days_until_page = page_number * WEEK_DAYS
    this_week_monday = date.today() - timedelta(days=date.today().weekday())
    next_week_monday = this_week_monday + timedelta(days=WEEK_DAYS)
    this_week_last_session_datetime = _this_week_last_session_datetime(
        this_week_monday, next_week_monday
    )
    page_zero_monday = (
        this_week_monday if datetime.now() <= this_week_last_session_datetime
        else next_week_monday
    )
    return page_zero_monday + timedelta(days=days_until_page)


def _this_week_last_session_datetime(this_week_monday, next_week_monday):
    this_week_monday_datetime = datetime.combine(
        this_week_monday, datetime.min.time())
    this_week_saturday = this_week_monday_datetime + timedelta(
        days=SATURDAY_TIMEDELTA_DAYS,
    )
    try:
        this_week_last_session = Session.objects.filter(
            date__gte=this_week_saturday, date__lte=next_week_monday,
        ).order_by('-date', '-hour__hour')[0]
        this_week_last_session_datetime = (
            this_week_last_session.datetime() + timedelta(hours=1))
    except IndexError:
        this_week_last_session_datetime = this_week_saturday + timedelta(
            hours=DEFAULT_LAST_SESSION_HOUR + 1,
        )
    return this_week_last_session_datetime


def is_too_late(session_id):
    try:
        session = Session.objects.get(pk=session_id)
        return date.today() >= session.date
    except Session.DoesNotExist:
        return True  # TODO: it's a lie
