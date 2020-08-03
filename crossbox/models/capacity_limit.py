from django.db import models


class CapacityLimit(models.Model):
    class Meta:
        verbose_name = 'Límite de Aforo'
        verbose_name_plural = 'Límites de Aforo'

    minimum = models.IntegerField('Mínimo')
    maximum = models.IntegerField('Máximo')
    default = models.BooleanField('Predeterminado', default=False)

    def __str__(self):
        return '{} - {}'.format(self.minimum, self.maximum)
