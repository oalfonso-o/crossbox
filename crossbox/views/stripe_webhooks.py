import os
import ssl
import json
import stripe
import smtplib
import logging
import functools
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
        mail_msg = other_event_mail_message(event)
        send_mail(mail_msg)
        return func(request, event)
    return wrapper_stripe_log_mail_event


def other_event_mail_message(webhook, event):
    receivers = [settings.SMTP_ADMIN_NOTIFICATIONS]
    return (
        f'''Subject:{webhook}: {event.type}\nTo:{receivers}
\n\nEvent body:
{json.dumps(event, indent=4)}''')


def payment_succeeded_message(receivers, fee):
    return (
        f'''Subject:Acabas de comprar wods!\nTo:{receivers}
\n\nHas comprado {fee.num_sessions} wods por {fee.price_cents / 100}€.
\n\nGracias!''')


def payment_failed_message(receivers):
    return (
        f'''Subject:No se ha podido procesar el pago de Crossbox\nTo:{receivers}
\n\nNo hemos podido procesar el pago de tu subscripción de Crossbox Palau.
 Comprueba que tengas activado un método de pago válido y si es así, ponte en
 contacto con nosotros y te lo solucionaremos.
\n\nGracias!''')


def send_mail(message, receivers):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        settings.SMTP_SERVER_NOTIFICATIONS,
        settings.SMTP_PORT_NOTIFICATIONS,
        context=context,
    ) as server:
        server.login(
            settings.SMTP_USER_NOTIFICATIONS,
            settings.SMTP_PASSWORD_NOTIFICATIONS,
        )
        server.sendmail(
            settings.SMTP_USER_NOTIFICATIONS,
            receivers.split(','),
            message,
        )


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
        subscriber.save()
        receivers = [
            subscriber.user.email,
            settings.SMTP_ADMIN_NOTIFICATIONS,
            settings.SMTP_BOSS_NOTIFICATIONS,
        ]
        mail_msg = payment_succeeded_message(receivers, fee)
        send_mail(mail_msg)
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
        mail_msg = payment_failed_message(receivers)
        send_mail(mail_msg)
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
@stripe_log_mail_event
def stripe_webhook_invoices(request, event):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_PLANS'))
@stripe_log_mail_event
def stripe_webhook_plans(request, event):
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
@stripe_log_mail_event
def stripe_webhook_customers(request, event):
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
