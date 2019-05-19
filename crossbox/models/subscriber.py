from django.db import models
from django.contrib.auth.models import User


class Subscriber(models.Model):
    class Meta:
        verbose_name = 'Abonado'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='subscriber')
    wods = models.IntegerField(default=0)

    def __str__(self):
        return '#{} - {}'.format(self.id, self.user)

    def username(self):
        return self.user.username

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name
