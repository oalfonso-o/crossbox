import os
import stripe
import logging
import functools
from dotenv import load_dotenv, find_dotenv

from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

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
        subscriber.stripe_next_payment_timestamp = next_payment_timestamp  # TODO: rename to stripe_next_payment_timestamp
        subscriber.wods = wods
        try:
            subscriber.save()
        except Exception as e:
            # TODO: mail -> uri
            logger.info('mail -> uri')
            raise e
        logger.info('mail -> roger uri customer')
        # TODO: mail -> roger uri customer
    else:
        logger.error(event)
        # TODO: mail -> uri
        logger.info('mail -> uri')
        return HttpResponse(status=400)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_PAYMENT_FAIL'))
def stripe_webhook_payment_fail(request, event):
    if event.type == 'invoice.payment_failed':
        logger.info(event)
        # TODO: mail -> roger uri customer
    else:
        logger.error(event)
        # TODO: mail -> uri
        logger.info('mail -> uri')
        return HttpResponse(status=400)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_CHARGES'))
def stripe_webhook_charges(request, event):
    logger.info(event)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_INVOICES'))
def stripe_webhook_invoices(request, event):
    logger.info(event)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_PLANS'))
def stripe_webhook_plans(request, event):
    logger.info(event)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_PRICES'))
def stripe_webhook_prices(request, event):
    logger.info(event)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_CUSTOMERS'))
def stripe_webhook_customers(request, event):
    logger.info(event)
    send_mail(
        'Subject here',
        'Here is the message.',
        'notifications@crossboxpalau.com',
        ['oriolalfonso91@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_CUSTOMER_SOURCES'))
def stripe_webhook_customer_sources(request, event):
    logger.info(event)
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
