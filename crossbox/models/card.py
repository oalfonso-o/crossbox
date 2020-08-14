import stripe

from django.db import models
from django.dispatch import receiver

from crossbox.models.subscriber import Subscriber


class Card(models.Model):
    class Meta:
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'

    last_digits = models.IntegerField('Últimos dígitos')
    default = models.BooleanField('Por defecto', default=False)
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.CASCADE, related_name='cards')
    stripe_card_id = models.CharField('ID Tarjeta Stripe', max_length=40)

    def __str__(self):
        return f'***{self.last_digits} - {self.subscriber}'


@receiver(models.signals.post_delete, sender=Card)
def delete_card(sender, instance, *args, **kwargs):
    stripe.Customer.delete_source(
        instance.subscriber.stripe_customer_id,
        instance.stripe_card_id,
    )
