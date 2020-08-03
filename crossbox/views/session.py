import datetime
from http import HTTPStatus

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseRedirect

from crossbox.models.track import Track
from crossbox.models.capacity_limit import CapacityLimit
from crossbox.models.session import Session
from crossbox.models.session_template import SessionTemplate
from crossbox.views.tools import get_monday_from_page, error_response
from crossbox.constants import SATURDAY_WEEK_DAY


def generate_sessions(request):
    page_num = request.POST.get('page')
    week_tmpl = request.POST.get('week_template')
    track = request.POST.get('track')
    capacity_limit = request.POST.get('capacity_limit')
    if all(p is None for p in(page_num, week_tmpl, track, capacity_limit)):
        raise Exception(
            f"Can't generate sessions, there is one empty field:"
            f"page_num: {page_num}, week_template: {week_tmpl}, "
            f"track: {track}, capacity_limit: {capacity_limit}"
        )
    track_obj = Track.objects.get(pk=track)
    capacity_limit_obj = CapacityLimit.objects.get(pk=capacity_limit)
    monday = get_monday_from_page(int(page_num))
    sunday = monday + datetime.timedelta(days=SATURDAY_WEEK_DAY)
    sessions_to_delete = Session.objects.filter(
        date__gte=monday, date__lte=sunday, track=track)
    sessions_to_delete.delete()
    future_sessions = (
        Session(
            date=monday + datetime.timedelta(days=st.day.weekday),
            hour=st.hour,
            track=track_obj,
            capacity_limit=capacity_limit_obj,
        )
        for st in SessionTemplate.objects.filter(week_template=week_tmpl))
    Session.objects.bulk_create(future_sessions)
    return HttpResponseRedirect('/reservation/?page={}'.format(page_num))


@require_http_methods(['PUT'])
def change_session_type(request, session_id):
    try:
        session = Session.objects.get(pk=session_id)
    except Session.DoesNotExist:
        return error_response(
            request, 'session_not_found', HTTPStatus.NOT_FOUND)
    next_session_type = session.set_next_session_type()
    return JsonResponse(
        {
            'session_type': {
                'pk': next_session_type.pk,
                'name': next_session_type.name,
            }
        }
    )
