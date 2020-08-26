import stripe
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

from crossbox.models.subscriber import Subscriber
from crossbox.views.stripe_webhooks import send_mail

logger = logging.getLogger(__name__)


@receiver(models.signals.pre_save, sender=User)
def user_pre_save(sender, instance, *args, **kwargs):
    if instance.pk:  # update existing
        db_instance = User.objects.get(pk=instance.pk)
        if UserModelHelper.user_has_been_activated(db_instance, instance):
            UserModelHelper.create_stripe_customer_and_subscriber(instance)
            UserModelHelper.send_activate_user_email(instance)
        elif UserModelHelper.user_has_been_deactivated(db_instance, instance):
            UserModelHelper.delete_stripe_customer(instance)
            instance.subscriber.delete()


class UserModelHelper:

    @staticmethod
    def user_has_been_activated(db_instance, new_instance):
        return bool(
            not db_instance.is_active
            and new_instance.is_active
        )

    @staticmethod
    def create_stripe_customer_and_subscriber(instance):
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

    @classmethod
    def send_activate_user_email(cls, user):
        msg = cls._get_mail_msg(user)
        receivers = [
            user.email,
            settings.SMTP_ADMIN_NOTIFICATIONS,
            settings.SMTP_BOSS_NOTIFICATIONS,
        ]
        send_mail(msg, receivers)

    @staticmethod
    def _get_mail_msg(user):
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Tu cuenta de Crossbox ha sido activada!'
        message['From'] = settings.SMTP_USER_NOTIFICATIONS
        message['To'] = user.email
        html = f'''\
    <html>
        <body>
            <p>Hola {user.first_name} {user.last_name}</p>
            <br>
            Acabamos de activar tu cuenta, ya puedes acceder a
            <a href="{settings.BASE_URL}">Crossbox!</a>
            <br>
            <br>
            <br>
            Atentamente,
            <br>
            El equipo de <a href="https://www.crossboxpalau.com/">
            Crossbox Palau</a>
        </p>
    </body>
    </html>'''
        html_part = MIMEText(html, 'html')
        message.attach(html_part)
        return message.as_string()

    @staticmethod
    def user_has_been_deactivated(db_instance, new_instance):
        return bool(
            db_instance.is_active
            and not new_instance.is_active
        )

    @staticmethod
    def delete_stripe_customer(instance):
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
