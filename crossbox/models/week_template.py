from django.db import models


class WeekTemplate(models.Model):
    class Meta:
        verbose_name = 'Plantilla de Semana'
        verbose_name_plural = 'Plantillas de Semana'

    name = models.CharField('Plantilla de semana', max_length=50, unique=True)
    default = models.BooleanField('Predeterminada', default=False)

    def __str__(self):
        return self.name
