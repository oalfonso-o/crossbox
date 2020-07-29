import itertools
from datetime import datetime

from django.db import models

from .hour import Hour
from .session_template import AppraisalLimit, Track


class Session(models.Model):
    WOD = 'wod'
    OPEN = 'open'
    STRETCHING = 'stre'
    SESSION_TYPES = [
        (WOD, 'WOD'),
        (OPEN, 'OPEN'),
        (STRETCHING, 'ESTIRAMIENTOS'),
    ]

    class Meta:
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
        unique_together = ('date', 'hour')

    date = models.DateField('Día', default=True)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE, null=False)
    session_type = models.CharField(
        max_length=4, choices=SESSION_TYPES, default=WOD)
    appraisal_limit = models.ForeignKey(
        AppraisalLimit, on_delete=models.PROTECT, null=False)
    track = models.ForeignKey(Track, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return '{} - {}:{}'.format(
            self.session_type, self.date, self.hour.hour_simple()
        )

    def datetime(self):
        return datetime.combine(self.date, self.hour.hour)

    def is_closed(self):
        return bool(self.datetime() < datetime.now())

    def set_next_session_type(self):
        types_cycle = itertools.cycle(self.SESSION_TYPES)
        for key, value in types_cycle:
            if self.session_type == key:
                next_type, _ = next(types_cycle)
                self.session_type = next_type
                self.save()
                break
