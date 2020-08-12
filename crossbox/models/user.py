import stripe
import logging

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from crossbox.models.subscriber import Subscriber

logger = logging.getLogger(__name__)


@receiver(models.signals.post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        stripe_customer = stripe.Customer.create(
            name=instance.username,
            email=instance.email,
            description=f'{instance.first_name} {instance.last_name}',
        )
        stripe_customer_id = stripe_customer['id']
        stripe_subscription_id = None
        Subscriber.objects.create(
            user=instance,
            wods=1,
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_subscription_id,
        )
    elif not instance.is_active:
        stripe_customer_id = instance.subscriber.stripe_customer_id
        try:
            response = stripe.Customer.delete(stripe_customer_id)
        except stripe.error.InvalidRequestError:
            logger.info(
                f'User {instance} is disabled and has no stripe customer')
            return
        if not response['deleted']:
            raise Exception(
                f'Customer {stripe_customer_id} could not be deleted of user '
                f'{instance}. More info: {response}'
            )
    else:
        stripe_customer = stripe.Customer.retrieve(
            instance.subscriber.stripe_customer_id)
        if 'deleted' in stripe_customer and stripe_customer['deleted']:
            stripe_customer = stripe.Customer.create(
                name=instance.username,
                email=instance.email,
                description=f'{instance.first_name} {instance.last_name}',
            )
            instance.subscriber.stripe_customer_id = stripe_customer['id']
            instance.subscriber.save()
