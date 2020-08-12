from django.db import models


class Fee(models.Model):
    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'

    num_sessions = models.IntegerField('Número de sesiones')
    price_cents = models.IntegerField('Precio en céntimos')
    stripe_product_id = models.IntegerField('ID Producto Stripe')
    active = models.BooleanField('Activa', default=True)

    def __str__(self):
        return (
            f'{self.num_sessions} sessions - cost {self.price_cents} cents - '
            f'Stripe Product ID: {self.stripe_product_id}'
        )
