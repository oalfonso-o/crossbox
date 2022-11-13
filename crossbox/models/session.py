import itertools
from datetime import datetime

from django.db import models

from crossbox.models.hour import Hour
from crossbox.models.track import Track
from crossbox.models.session_type import SessionType
from crossbox.models.capacity_limit import CapacityLimit


class Session(models.Model):
    DEFAULT_SESSION_TYPE_ID = 1

    class Meta:
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
        unique_together = ('date', 'hour', 'track')

    date = models.DateField('Día', default=True)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE, null=False)
    session_type = models.ForeignKey(
        SessionType,
        on_delete=models.CASCADE,
        null=False,
        default=DEFAULT_SESSION_TYPE_ID,
    )
    capacity_limit = models.ForeignKey(
        CapacityLimit, on_delete=models.PROTECT, null=False)
    track = models.ForeignKey(Track, on_delete=models.PROTECT, null=False)
    discount = models.BooleanField('Horario descuento', default=False)

    def __str__(self):
        return '{} - {} - {}'.format(
            self.session_type.name, self.date, self.hour.hour_simple()
        )

    def datetime(self):
        return datetime.combine(self.date, self.hour.hour)

    def weekday(self):
        return self.date.strftime('%A')

    def is_closed(self):
        return bool(self.datetime() < datetime.now())

    def set_next_session_type(self):
        session_types = SessionType.objects.all().order_by('pk')
        types_cycle = itertools.cycle(session_types)
        for session_type in types_cycle:
            if self.session_type.pk == session_type.pk:
                next_type = next(types_cycle)
                self.session_type = next_type
                self.save()
                return next_type
