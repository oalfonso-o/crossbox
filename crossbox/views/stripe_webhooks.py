import os
import ssl
import json
import stripe
import smtplib
import logging
import functools
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv, find_dotenv

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from crossbox.models.fee import Fee
from crossbox.models.subscriber import Subscriber

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)


def stripe_event(endpoint_secret):
    def decorator_stripe_event(func):
        @functools.wraps(func)
        def wrapper_stripe_event(request):
            payload = request.body
            sig_header = request.META['HTTP_STRIPE_SIGNATURE']
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
            return func(request, event)
        return wrapper_stripe_event
    return decorator_stripe_event


def stripe_log_mail_event(func):
    @functools.wraps(func)
    def wrapper_stripe_log_mail_event(request, event):
        logger.info(event)
        receivers = [
            settings.SMTP_ADMIN_NOTIFICATIONS,
            settings.SMTP_BOSS_NOTIFICATIONS,
        ]
        mail_msg = other_event_mail_message(event, receivers)
        send_mail(mail_msg, receivers)
        return func(request, event)
    return wrapper_stripe_log_mail_event


def other_event_mail_message(event, receivers):
    message = MIMEMultipart('alternative')
    message['Subject'] = f'Crossbox event: {event.type}'
    message['From'] = settings.SMTP_USER_NOTIFICATIONS
    message['To'] = ', '.join(receivers)
    html = f'''\
<html>
    <body>
        <p>Hei admin, aquí tienes un nuevo evento:</p>
        <br>
            <pre>
{json.dumps(event, indent=4)}
            </pre>
        <br>
        Disfrútalo ;)
        <br>
        <br>
        Atentamente,
        <br>
        El equipo de <a href="https://www.crossboxpalau.com/">Crossbox Palau
        </a>
    </p>
  </body>
</html>'''
    html_part = MIMEText(html, 'html')
    message.attach(html_part)
    return message.as_string()


def payment_succeeded_message(fee, receivers, username):
    message = MIMEMultipart('alternative')
    message['Subject'] = (
        f'{username} acabas de comprar {fee.num_sessions} wods!')
    message['From'] = settings.SMTP_USER_NOTIFICATIONS
    message['To'] = ', '.join(receivers)
    html = f'''\
<html>
    <body>
        <p>Hei, te notificamos que hemos recibido tu pago!</p>
        <p>Has comprado <b>{fee.num_sessions}</b> wods por
        <b>{fee.price_cents / 100}€</b>
        </p>
        Recuerda que siempre puedes modificar tu cuota des de tu
        <a href="{settings.BASE_URL}/profile/">perfil</a>.
        <br>
        <br>
        Muchas gracias!
        <br>
        <br>
        Atentamente,
        <br>
        El equipo de <a href="https://www.crossboxpalau.com/">Crossbox Palau
        </a>
    </p>
  </body>
</html>'''
    html_part = MIMEText(html, 'html')
    message.attach(html_part)
    return message.as_string()


def payment_failed_message(receivers, username):
    message = MIMEMultipart('alternative')
    message['Subject'] = (
        f'{username} no hemos podido procesar tu pago de Crossbox :(')
    message['From'] = settings.SMTP_USER_NOTIFICATIONS
    message['To'] = ', '.join(receivers)
    html = f'''\
<html>
    <body>
        <p>Hei, lamentablemente no hemos podido procesar el pago de tu cuota.
        </p>
        <p>Es posible que tu método de pago haya caducado o que lo hayas
        eliminado de tu perfil. Comprueba que tengas un método de pago
        válido activado en tu
        <a href="{settings.BASE_URL}/profile/">perfil</a> y
        si no recibes confirmación del pago
        en las próximas horas ponte en contacto con nosotros directamente por
        whatsapp o mandando un mail a
        <a href="{settings.SMTP_BOSS_NOTIFICATIONS}">
        {settings.SMTP_BOSS_NOTIFICATIONS}</a>.
        </p>
        <br>
        <br>
        Muchas gracias!
        <br>
        <br>
        Atentamente,
        <br>
        El equipo de <a href="https://www.crossboxpalau.com/">Crossbox Palau
        </a>
    </p>
  </body>
</html>'''
    html_part = MIMEText(html, 'html')
    message.attach(html_part)
    return message.as_string()


def send_mail(message, receivers):
    context = ssl.create_default_context()
    with smtplib.SMTP(
        settings.SMTP_SERVER_NOTIFICATIONS,
        settings.SMTP_PORT_NOTIFICATIONS,
    ) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(
            settings.SMTP_USER_NOTIFICATIONS,
            settings.SMTP_PASSWORD_NOTIFICATIONS,
        )
        server.sendmail(settings.SMTP_USER_NOTIFICATIONS, receivers, message)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_PAYMENT_OK'))
def stripe_webhook_payment_ok(request, event):
    if event.type == 'invoice.payment_succeeded':
        logger.info(event)
        event_data_obj = event.data.object
        line_data_first = event_data_obj.lines.data[0]
        price_id = line_data_first.price.id
        fee = Fee.objects.get(stripe_price_id=price_id)
        wods = fee.num_sessions
        paid_timestamp = event_data_obj.status_transitions.paid_at
        subscription_id = event_data_obj.subscription
        subscription = stripe.Subscription.retrieve(subscription_id)
        next_payment_timestamp = subscription.current_period_end

        customer_id = event_data_obj.customer
        subscriber = Subscriber.objects.get(stripe_customer_id=customer_id)
        subscriber.stipe_last_payment_timestamp = paid_timestamp
        subscriber.stripe_next_payment_timestamp = next_payment_timestamp
        subscriber.wods = wods
        if not fee.active:
            subscriber.fee = None
        subscriber.save()
        receivers = [
            subscriber.user.email,
            settings.SMTP_ADMIN_NOTIFICATIONS,
            settings.SMTP_BOSS_NOTIFICATIONS,
        ]
        mail_msg = payment_succeeded_message(
            fee, receivers, subscriber.user.username)
        send_mail(mail_msg, receivers)
    else:
        logger.error(event)
        return HttpResponse(status=400)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_PAYMENT_FAIL'))
def stripe_webhook_payment_fail(request, event):
    if event.type == 'invoice.payment_failed':
        logger.info(event)
        event_data_obj = event.data.object
        customer_id = event_data_obj.customer
        subscriber = Subscriber.objects.get(stripe_customer_id=customer_id)
        receivers = [
            subscriber.user.email,
            settings.SMTP_ADMIN_NOTIFICATIONS,
            settings.SMTP_BOSS_NOTIFICATIONS,
        ]
        mail_msg = payment_failed_message(receivers, subscriber.user.username)
        send_mail(mail_msg, receivers)
    else:
        logger.error(event)
        return HttpResponse(status=400)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_CHARGES'))
@stripe_log_mail_event
def stripe_webhook_charges(request, event):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_INVOICES'))
def stripe_webhook_invoices(request, event):
    # MAILS DEACTIVATED
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_PLANS'))
def stripe_webhook_plans(request, event):
    # MAILS DEACTIVATED
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_PRICES'))
@stripe_log_mail_event
def stripe_webhook_prices(request, event):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_CUSTOMERS'))
def stripe_webhook_customers(request, event):
    # MAILS DEACTIVATED
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_CUSTOMER_SOURCES'))
@stripe_log_mail_event
def stripe_webhook_customer_sources(request, event):
    return HttpResponse(status=200)


STRIPE_WEBHOOKS_VIEWS_MAPPER = {
    'stripe_webhook_payment_ok': stripe_webhook_payment_ok,
    'stripe_webhook_payment_fail': stripe_webhook_payment_fail,
    'stripe_webhook_charges': stripe_webhook_charges,
    'stripe_webhook_invoices': stripe_webhook_invoices,
    'stripe_webhook_plans': stripe_webhook_plans,
    'stripe_webhook_prices': stripe_webhook_prices,
    'stripe_webhook_customers': stripe_webhook_customers,
    'stripe_webhook_customer_sources': stripe_webhook_customer_sources,
}
