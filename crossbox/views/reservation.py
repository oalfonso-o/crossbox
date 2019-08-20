import locale
import json
from http import HTTPStatus
from datetime import timedelta

from django.views.generic.list import ListView
from django.http import JsonResponse
from django.db import IntegrityError

from crossbox.models import Reservation, Session, Hour
from .tools import active_page_number, get_monday_from_page, is_too_late
from crossbox.constants import (
    MIDWEEK_DAYS,
    SATURDAY_WEEK_DAY,
    MAX_RESERVATION_PLACES,
)


class ReservationView(ListView):
    model = Reservation
    template_name = 'reservation_list.html'

    def get_context_data(self, **kwargs):
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        context = super(ReservationView, self).get_context_data(**kwargs)
        page_number = active_page_number(self.request)
        monday = get_monday_from_page(page_number)
        saturday = monday + timedelta(days=MIDWEEK_DAYS)
        sessions = Session.objects.filter(date__gte=monday, date__lte=saturday)
        hour_pks = sessions.values('hour__pk').distinct()
        days = [monday + timedelta(days=i) for i in range(SATURDAY_WEEK_DAY)]
        context['hours'] = Hour.objects.filter(
            pk__in=hour_pks).order_by('hour')
        context['days'] = [self.row_object(d, context['hours']) for d in days]
        context['from_date'] = monday
        context['to_date'] = saturday
        context['page'] = page_number
        context['wods'] = getattr(self.request.user.subscriber, 'wods')
        return context

    def row_object(self, d, hours):
        data = [d]
        for h in hours:
            session = Session.objects.filter(date=d, hour=h).first()
            record = {
                'user_reservated': self.user_has_reservated(session),
                'session': session.id if session else None,
                'session_closed': session.is_closed() if session else None,
                'hour': h.hour_simple(),
                'reservations': (
                    self.username_reservations(session) if session else [])}
            data.append(record)
        return data

    def username_reservations(self, session):
        return [r.user.username for r in session.reservations.all()]

    def user_has_reservated(self, session):
        return (
            bool(Reservation.objects.filter(
                session=session.id, user=self.request.user).first())
            if session else False
        )


def reservation_create(request):
    wods = getattr(request.user.subscriber, 'wods')
    if wods is None or wods < 1:
        return _error_response(request, 'no_wods', HTTPStatus.FORBIDDEN)
    data = json.loads(request.body)
    session = Session.objects.get(pk=data['session'])
    if session.reservations.count() >= MAX_RESERVATION_PLACES:
        return _error_response(
            request, 'max_reservations', HTTPStatus.FORBIDDEN)
    reservation = Reservation()
    reservation.user = request.user
    reservation.session = session
    try:
        reservation.save()
        request.user.subscriber.wods -= 1
        request.user.subscriber.save()
    except IntegrityError:
        return _error_response(
            request, 'already_reserved', HTTPStatus.FORBIDDEN)
    return JsonResponse(
        {
            'result': 'created', 'username': request.user.username,
            'wods': request.user.subscriber.wods,
        }
    )


def _error_response(request, msg, code):
    return JsonResponse(
        {'result': msg, 'username': request.user.username},
        status=code,
    )


def reservation_delete(request):
    data = json.loads(request.body)
    # TODO: check if session exists, now is returning is_too_late if not found
    if is_too_late(data['session']):
        return _error_response(request, 'is_too_late', HTTPStatus.FORBIDDEN)
    wods = getattr(request.user.subscriber, 'wods')
    if wods is None:
        return _error_response(request, 'no_subscriber', HTTPStatus.FORBIDDEN)
    try:
        reservation = Reservation.objects.get(
            session=data['session'], user=request.user)
    except Reservation.DoesNotExist:
        return _error_response(
            request, 'no_reservation', HTTPStatus.NOT_FOUND)
    if not reservation.session.is_closed():
        reservation.delete()
        request.user.subscriber.wods += 1
        request.user.subscriber.save()
        return JsonResponse({
            'result': 'deleted', 'username': request.user.username,
            'wods': request.user.subscriber.wods})
    else:
        return _error_response(request, 'is_too_late', HTTPStatus.FORBIDDEN)
    return _error_response(request, 'unhandled', HTTPStatus.BAD_REQUEST)
