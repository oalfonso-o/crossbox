from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from crossbox.models.subscriber import Subscriber


@receiver(models.signals.post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        Subscriber.objects.create(user=instance, wods=1)
