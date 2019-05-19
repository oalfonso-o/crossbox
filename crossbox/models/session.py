from datetime import datetime

from django.db import models

from .hour import Hour


class Session(models.Model):
    class Meta:
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
        unique_together = ('date', 'hour')

    date = models.DateField('Día', default=True)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{} - {}'.format(self.date, self.hour.hour_simple())

    def datetime(self):
        return datetime.combine(self.date, self.hour.hour)

    def is_closed(self):
        return bool(self.datetime() < datetime.now())
