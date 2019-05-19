from django.db import models

from .day import Day
from .hour import Hour


class SessionTemplate(models.Model):
    class Meta:
        verbose_name = 'Plantilla de Sesión'
        verbose_name_plural = 'Plantillas de Sesión'
        unique_together = ('day', 'hour')

    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=False)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{} - {}'.format(self.day, self.hour.hour_simple())
