from django.db import models


class SessionType(models.Model):
    class Meta:
        verbose_name = 'Tipo de Sesión'
        verbose_name_plural = 'Tipos de Sesión'

    name = models.CharField('Tipo de sesión', max_length=50, unique=True)
    default = models.BooleanField('Predeterminado', default=False)
