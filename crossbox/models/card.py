from django.db import models

from crossbox.models.subscriber import Subscriber


class Card(models.Model):
    class Meta:
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'

    last_digits = models.IntegerField('Últimos dígitos')
    active = models.BooleanField('Activa', default=False)
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return f'***{self.last_digits} - {self.subscriber}'
