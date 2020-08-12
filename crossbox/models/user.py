import stripe

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from crossbox.models.subscriber import Subscriber


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


@receiver(models.signals.pre_delete, sender=User)
def user_pre_delete(sender, instance, using, **kwargs):
    stripe_customer_id = instance.subscriber.stripe_customer_id
    response = stripe.Customer.delete(stripe_customer_id)
    if not response['deleted']:
        raise Exception(
            f'Customer {stripe_customer_id} could not be deleted of user '
            f'{instance}. More info: {response}'
        )
