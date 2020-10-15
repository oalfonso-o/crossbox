from django.db import models

from crossbox.models.subscriber import Subscriber


class Card(models.Model):
    class Meta:
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'

    last_digits = models.CharField('Últimos dígitos', max_length=4)
    default = models.BooleanField('Por defecto', default=False)
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.CASCADE, related_name='cards')
    stripe_card_id = models.CharField('ID Tarjeta Stripe', max_length=40)

    def __str__(self):
        return f'***{self.last_digits} - {self.subscriber}'
