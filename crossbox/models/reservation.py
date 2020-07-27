from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html

from crossbox.exceptions import LimitExceeed
from crossbox.constants import MAX_RESERVATION_PLACES


class Reservation(models.Model):
    class Meta:
        verbose_name = 'Reserva'
        unique_together = ('user', 'session')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reservations')
    session = models.ForeignKey(
        'session', on_delete=models.CASCADE, related_name='reservations')
    refund = models.BooleanField('Devolución', default=False)

    def user_info(self):
        return format_html(
            '<span style="color: green;">{}: </span>{} {}',
            self.user.username,
            self.user.first_name,
            self.user.last_name,
        )

    def __str__(self):
        return (
            '{} {}'.format(self.user.first_name, self.user.last_name)
            if self.user.first_name
            else self.user.username
        )

    def save(self, *args, **kwargs):
        if self.session.reservations.count() < MAX_RESERVATION_PLACES:
            super(Reservation, self).save(*args, **kwargs)
        else:
            raise LimitExceeed('Maximum reservations for this session')
