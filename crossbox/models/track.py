from django.db import models


class Track(models.Model):
    class Meta:
        verbose_name = 'Pista'
        verbose_name_plural = 'Pistas'

    name = models.CharField('Pista', max_length=250, unique=True)
    default = models.BooleanField('Predeterminada', default=False)

    def __str__(self):
        return self.name
