import logging

from django.db import models

logger = logging.getLogger(__name__)


class Fee(models.Model):
    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'

    num_sessions = models.IntegerField('Número de sesiones')
    price_cents = models.IntegerField('Precio en céntimos')
    active = models.BooleanField('Activa', default=True)
    morning = models.BooleanField('Sesión de mañana', default=False)

    def label_property(self):
        if not self.num_sessions:
            return f'Cuota de mantenimiento {self.price_cents / 100}€'
        if self.morning:
            return f'Cuota de mañanas {self.price_cents / 100}€'
        num_sessions = '∞' if self.num_sessions >= 50 else self.num_sessions
        return f'{num_sessions} sesiones - {self.price_cents / 100}€'

    label_property.short_description = "Cuota"
    label = property(label_property)

    def __str__(self):
        return self.label
