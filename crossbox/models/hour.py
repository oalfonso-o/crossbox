from datetime import time

from django.db import models

from crossbox.constants import SIMPLE_TIME_POS


class Hour(models.Model):
    class Meta:
        verbose_name = 'Hora'

    hour = models.TimeField('Hora de la sesión', unique=True)

    def __str__(self):
        return self.hour_range()

    def hour_range(self):
        next_hour_int = self.hour.hour + 1 if self.hour.hour < 23 else 0
        return '{} - {}'.format(
            self.hour.isoformat()[:SIMPLE_TIME_POS],
            time(
                hour=next_hour_int, minute=self.hour.minute
            ).isoformat()[:SIMPLE_TIME_POS]
        )
    hour_range.short_description = 'Rango de horas'

    def hour_simple(self):
        return self.hour.isoformat()[:SIMPLE_TIME_POS]
    hour_simple.short_description = 'Hora'
