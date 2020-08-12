from django.db import models
from django.contrib.auth.models import User

from crossbox.models.fee import Fee


class Subscriber(models.Model):
    class Meta:
        verbose_name = 'Abonado'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='subscriber')
    wods = models.IntegerField(default=0)
    fee = models.ForeignKey(
        Fee, on_delete=models.PROTECT, null=True, related_name='subscribers')
    stripe_customer_id = models.IntegerField(
        'ID Cliente Stripe', blank=False, null=True)
    stripe_subscription_id = models.IntegerField(
        'ID Subscripción Stripe', blank=False, null=True)

    def __str__(self):
        return '#{} - {}'.format(self.id, self.user)

    def username(self):
        return self.user.username

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name
