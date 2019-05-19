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
        return '{} - {}'.format(
            self.hour.isoformat()[:SIMPLE_TIME_POS],
            time(
                hour=self.hour.hour + 1,
                minute=self.hour.minute).isoformat()[:SIMPLE_TIME_POS]
            )
    hour_range.short_description = 'Rango de horas'

    def hour_simple(self):
        return self.hour.isoformat()[:SIMPLE_TIME_POS]
    hour_simple.short_description = 'Hora'
