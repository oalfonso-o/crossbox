import os
import stripe
import logging
import functools
from dotenv import load_dotenv, find_dotenv

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)


def stripe_event(endpoint_secret):
    def decorator_stripe_event(func):
        @functools.wraps(func)
        def wrapper_stripe_event(request):
            logger.info('in wrapper')
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
    logger.info(event)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_PAYMENT_FAIL'))
def stripe_webhook_payment_fail(request, event):
    logger.info(event)
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
    # Handle the event
    # if event.type == 'payment_intent.succeeded':
    #     payment_intent = event.data.object # contains a stripe.PaymentIntent
    #     print('PaymentIntent was successful!')
    # elif event.type == 'payment_method.attached':
    #     payment_method = event.data.object # contains a stripe.PaymentMethod
    #     print('PaymentMethod was attached to a Customer!')
    # # ... handle other event types
    # else:
    #     # Unexpected event type
    #     return HttpResponse(status=400)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_event(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_CUSTOMER_SOURCES'))
def stripe_webhook_customer_sources(request, event):
    logger.info(event)
    return HttpResponse(status=200)
