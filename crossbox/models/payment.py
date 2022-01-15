from django.db import models

from crossbox.models.fee import Fee
from crossbox.models.subscriber import Subscriber


class Payment(models.Model):

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    subscriber = models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    fee = models.ForeignKey(Fee, on_delete=models.PROTECT)
    datetime = models.DateTimeField('Día y hora')
    payed_amount = models.IntegerField('Precio pagado')
    wods = models.IntegerField('Wods')
    stripe_error = models.BooleanField(
        'Error al pagar en Stripe',
        default=False,
    )

    def __str__(self):
        return '{} - {} - {}'.format(
            self.subscriber.user.username, self.fee.label, self.datetime
        )
