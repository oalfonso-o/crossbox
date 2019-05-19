import json
from datetime import timedelta

from django.views.generic.list import ListView
from django.http import HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse

from crossbox.models import Session, Hour, SessionTemplate, Day
from .tools import active_page_number, get_monday_from_page, is_too_late
from .constants import SATURDAY_WEEK_DAY


class SessionTemplateView(ListView):
    model = SessionTemplate
    template_name = 'session_template_list.html'

    def get_context_data(self, **kwargs):
        context = super(SessionTemplateView, self).get_context_data(**kwargs)
        hours = Hour.objects.order_by('hour').all()
        days = Day.objects.all()
        context['hours'] = hours
        context['days'] = [self.row_object(d, hours) for d in days]
        return context

    def row_object(self, d, hours):
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
    sunday = monday + timedelta(days=SATURDAY_WEEK_DAY)
    sessions_to_delete = Session.objects.filter(
        date__gte=monday, date__lte=sunday)
    sessions_to_delete.delete()
    future_sessions = (
        Session(date=monday + timedelta(days=st.day.weekday), hour=st.hour)
        for st in SessionTemplate.objects.all())
    Session.objects.bulk_create(future_sessions)
    return HttpResponseRedirect('/reservation/?page={}'.format(page_number))


def get_is_too_late(request):
    data = json.loads(request.read().decode())
    return JsonResponse({'is_too_late': is_too_late(data['session'])})
