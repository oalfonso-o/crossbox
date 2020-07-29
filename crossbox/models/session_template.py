from django.db import models

from .day import Day
from .hour import Hour


class Track(models.Model):
    class Meta:
        verbose_name = 'Pista'
        verbose_name_plural = 'Pistas'

    name = models.CharField('Pista', max_length=250, unique=True)
    default = models.BooleanField('Predeterminada', default=False)

    def __str__(self):
        return self.name


class WeekTemplate(models.Model):
    class Meta:
        verbose_name = 'Plantilla de Semana'
        verbose_name_plural = 'Plantillas de Semana'

    name = models.CharField('Plantilla de semana', max_length=50, unique=True)
    default = models.BooleanField('Predeterminada', default=False)

    def __str__(self):
        return self.name


class SessionTemplate(models.Model):
    class Meta:
        verbose_name = 'Plantilla de Sesión'
        verbose_name_plural = 'Plantillas de Sesión'
        unique_together = ('day', 'hour')

    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=False)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE, null=False)
    week_template = models.ForeignKey(
        WeekTemplate, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{} - {}'.format(self.day, self.hour.hour_simple())


class AppraisalLimit(models.Model):
    class Meta:
        verbose_name = 'Límite de Aforo'
        verbose_name_plural = 'Límites de Aforo'

    minimum = models.IntegerField('Mínimo')
    maximum = models.IntegerField('Máximo')
    default = models.BooleanField('Predeterminado', default=False)

    def __str__(self):
        return '{} - {}'.format(self.minimum, self.maximum)
