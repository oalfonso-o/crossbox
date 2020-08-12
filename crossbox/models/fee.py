import stripe
import logging

from django.db import models
from django.dispatch import receiver

logger = logging.getLogger(__name__)


class Fee(models.Model):
    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'

    num_sessions = models.IntegerField('Número de sesiones')
    price_cents = models.IntegerField('Precio en céntimos')
    stripe_product_id = models.CharField('ID Producto Stripe', max_length=30)
    stripe_price_id = models.CharField('ID Precio Stripe', max_length=30)
    active = models.BooleanField('Activa', default=True)

    def __str__(self):
        return (f'{self.num_sessions} sesiones - {self.price_cents / 100}€')


@receiver(models.signals.pre_save, sender=Fee)
def fee_pre_save(sender, instance, *args, **kwargs):
    existing_fees = Fee.objects.filter(pk=instance.pk).count()
    if not existing_fees:
        existing_products_response = stripe.Product.list()
        existing_products = existing_products_response.get('data', [])
        if not existing_products:
            product_name = 'Subscripción Mensual'
            product_description = (
                'Cuota de subscripción mensual a Crossbox Palau, el precio '
                'depende de la cantidad de sesiones contratadas')
            stripe_fee = stripe.Product.create(
                name=product_name,
                description=product_description,
            )
            instance.stripe_product_id = stripe_fee['id']
        elif len(existing_products) > 1:
            raise Exception(
                f'Something went wrong, we have more than one product in '
                f'stripe, here the list of poducts: '
                f'{existing_products_response}')
        else:
            instance.stripe_product_id = existing_products[0]['id']
        stripe_price = stripe.Price.create(
            unit_amount=instance.price_cents,
            currency='eur',
            recurring={'interval': 'month'},
            product=instance.stripe_product_id,
        )
        instance.stripe_price_id = stripe_price['id']
    elif not instance.active:
        stripe_price_id = instance.stripe_price_id
        stripe.Price.modify(stripe_price_id, active=False)
    else:
        stripe_price_id = instance.stripe_price_id
        stripe_price = stripe.Price.retrieve(stripe_price_id)
        if 'active' in stripe_price and not stripe_price['active']:
            stripe.Price.modify(stripe_price_id, active=True)
