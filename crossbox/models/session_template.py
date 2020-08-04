from django.db import models

from crossbox.models.day import Day
from crossbox.models.hour import Hour
from crossbox.models.week_template import WeekTemplate
from crossbox.models.capacity_limit import CapacityLimit


class SessionTemplate(models.Model):
    class Meta:
        verbose_name = 'Plantilla de Sesión'
        verbose_name_plural = 'Plantillas de Sesión'
        unique_together = ('day', 'hour', 'week_template')

    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=False)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE, null=False)
    week_template = models.ForeignKey(
        WeekTemplate, on_delete=models.CASCADE, null=False)
    capacity_limit = models.ForeignKey(
        CapacityLimit, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return '{} - {}'.format(self.day, self.hour.hour_simple())
