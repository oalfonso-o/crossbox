import datetime
from http import HTTPStatus

from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView
from django.http import JsonResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse

from crossbox.models import Session, Hour, SessionTemplate, Day
from crossbox.constants import (
    SATURDAY_WEEK_DAY,
    NUM_WEEKS_IN_A_YEAR,
    WEEK_DAYS,
)
from .tools import (
    active_page_number,
    get_monday_from_page,
    error_response,
)


class SessionTemplateView(ListView):
    model = SessionTemplate
    template_name = 'session_template_list.html'

    def get_context_data(self, **kwargs):
        context = super(SessionTemplateView, self).get_context_data(**kwargs)
        hours = Hour.objects.order_by('hour').all()
        days = Day.objects.all()
        context['hours'] = hours
        context['days'] = [self._row_object(d, hours) for d in days]
        context['weeks'] = self._weeks()
        return context

    def _row_object(self, d, hours):
        data = [d]
        for h in hours:
            session = SessionTemplate.objects.filter(day=d, hour=h).first()
            data.append({
                'session': session.id if session else None,
                'day': d.id,
                'hour': h.id,
                'hour_title': h.hour_simple(),
            })
        return data

    @staticmethod
    def _weeks():
        monday = get_monday_from_page(0)
        weeks = [
            (i, monday + datetime.timedelta(days=i * WEEK_DAYS))
            for i in range(NUM_WEEKS_IN_A_YEAR)
        ]
        return {
            num: (
                f'Lunes {monday.day}/{monday.month}/{monday.year} - Semana '
                f'{num + 1 if num else "1 (actual)"}'
            )
            for num, monday
            in weeks
        }


def session_template_create(request):
    session = SessionTemplate()
    session.day = Day.objects.get(pk=request.POST.get('day'))
    session.hour = Hour.objects.get(pk=request.POST.get('hour'))
    try:
        session.save()
    except IntegrityError:
        pass
    return HttpResponseRedirect(reverse('session-template'))


def session_template_delete(request):
    session = SessionTemplate.objects.get(pk=request.POST.get('session'))
    session.delete()
    return HttpResponseRedirect(reverse('session-template'))


def generate_sessions(request):
    page_number = active_page_number(request)
    monday = get_monday_from_page(page_number)
    sunday = monday + datetime.timedelta(days=SATURDAY_WEEK_DAY)
    sessions_to_delete = Session.objects.filter(
        date__gte=monday, date__lte=sunday)
    sessions_to_delete.delete()
    future_sessions = (
        Session(
            date=monday + datetime.timedelta(days=st.day.weekday),
            hour=st.hour
        )
        for st in SessionTemplate.objects.all())
    Session.objects.bulk_create(future_sessions)
    return HttpResponseRedirect('/reservation/?page={}'.format(page_number))


@require_http_methods(['PUT'])
def change_session_type(request, session_id):
    try:
        session = Session.objects.get(pk=session_id)
    except Session.DoesNotExist:
        return error_response(
            request, 'session_not_found', HTTPStatus.NOT_FOUND)
    session.set_next_session_type()
    return JsonResponse({'session_type': session.get_session_type_display()})
