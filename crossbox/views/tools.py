from datetime import date, timedelta

from crossbox.models import Session
from crossbox.constants import WEEK_DAYS, SATURDAY_WEEK_DAY


def active_page_number(request):
    first_page = 0
    return int(request.GET.get('page', first_page) or first_page)


def get_monday_from_page(page_number):
    days_until_page = page_number * WEEK_DAYS
    this_week_monday = date.today() - timedelta(days=date.today().weekday())
    next_week_monday = this_week_monday + timedelta(days=WEEK_DAYS)
    page_zero_monday = (
        this_week_monday if date.today().weekday() < SATURDAY_WEEK_DAY
        else next_week_monday
    )
    return page_zero_monday + timedelta(days=days_until_page)


def is_too_late(session_id):
    try:
        session = Session.objects.get(pk=session_id)
        return date.today() >= session.date
    except Session.DoesNotExist:
        return True  # TODO: it's a lie
