from django.db import models


class Day(models.Model):
    class Meta:
        verbose_name = 'Día'

    def __str__(self):
        return self.name

    name = models.CharField('Día de la semana', max_length=20, unique=True)
    weekday = models.IntegerField(
        'Número de día de la semana (Lunes es 0)', unique=True)
