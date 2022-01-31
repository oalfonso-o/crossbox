import datetime
import distutils

from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse

from crossbox.models.day import Day
from crossbox.models.hour import Hour
from crossbox.models.week_template import WeekTemplate
from crossbox.models.track import Track
from crossbox.models.capacity_limit import CapacityLimit
from crossbox.models.session_template import SessionTemplate
from crossbox.constants import NUM_WEEKS_IN_A_YEAR, WEEK_DAYS
from crossbox.views.tools import get_monday_from_page


class SessionTemplateView(ListView):
    model = SessionTemplate
    template_name = 'session_template_list.html'

    def get_context_data(self, **kwargs):
        context = super(SessionTemplateView, self).get_context_data(**kwargs)
        week_template_id = self.request.GET.get('week_template')
        if week_template_id:
            week_template = WeekTemplate.objects.get(pk=week_template_id)
        else:
            week_template = WeekTemplate.objects.filter(default=True).first()
            if not week_template:
                week_template = WeekTemplate.objects.first()
            if not week_template:
                raise Exception('Week template not found')
        hours = Hour.objects.order_by('hour').all()
        days = Day.objects.all()
        context['hours'] = hours
        context['days'] = [
            self._row_object(d, hours, week_template) for d in days
        ]
        context['weeks'] = self._weeks()
        context['week_templates'] = list(
            WeekTemplate.objects.order_by('-default'))
        context['current_week_template'] = week_template.pk
        context['tracks'] = Track.objects.all()
        current_track = 1
        for track in context['tracks']:
            if track.default is True:
                current_track = track.pk
                break
        context['current_track'] = current_track
        context['capacity_limits'] = CapacityLimit.objects.all()
        return context

    def _row_object(self, d, hours, week_template):
        data = [d]
        default_capacity_limit = CapacityLimit.objects.filter(
            default=True).first()
        if not default_capacity_limit:
            default_capacity_limit = CapacityLimit.objects.all().first()
        for h in hours:
            session = SessionTemplate.objects.filter(
                day=d, hour=h, week_template=week_template).first()
            data.append({
                'session': session.id if session else None,
                'day': d.id,
                'hour': h.id,
                'hour_title': h.hour_simple(),
                'morning': session.morning if session else False,
                'capacity_limit': (
                    session.capacity_limit.pk
                    if session
                    else default_capacity_limit.pk
                ),
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
    week_template = request.POST.get('week_template')
    session = SessionTemplate()
    session.day = Day.objects.get(pk=request.POST.get('day'))
    session.hour = Hour.objects.get(pk=request.POST.get('hour'))
    session.week_template = WeekTemplate.objects.get(pk=week_template)
    session.morning = distutils.util.strtobool(
        request.POST.get('morning', 'off')
    )
    session.capacity_limit = CapacityLimit.objects.get(
        pk=request.POST.get('capacity_limit'))
    session.save()
    return HttpResponseRedirect(
        f'{reverse("session-template")}?week_template={week_template}'
    )


def session_template_delete(request):
    week_template = request.POST.get('week_template')
    session = SessionTemplate.objects.get(pk=request.POST.get('session'))
    session.delete()
    return HttpResponseRedirect(
        f'{reverse("session-template")}?week_template={week_template}'
    )


def session_template_switch(request):
    week_template = request.POST.get('week_template')
    return HttpResponseRedirect(
        f'{reverse("session-template")}?week_template={week_template}'
    )
