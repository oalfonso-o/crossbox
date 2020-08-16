import os
import stripe
import logging
import functools

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

STRIPE_IPS = [
    'api.stripe.com',
    'checkout.stripe.com',
    'js.stripe.com',
    'm.stripe.com',
    'm.stripe.network',
    'q.stripe.com',
]


def stripe_secure(endpoint_secret):
    def decorator_stripe_secure(func):
        @functools.wraps(func)
        def wrapper_stripe_secure(request):
            if request.META['REMOTE_ADDR'] not in STRIPE_IPS:
                return HttpResponse(status=400)
            payload = request.body
            sig_header = request.META['HTTP_STRIPE_SIGNATURE']
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
            return func(request, event)
        return wrapper_stripe_secure
    return decorator_stripe_secure


@csrf_exempt
@require_POST
def stripe_webhook_payment_ok(request):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def stripe_webhook_payment_fail(request):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def stripe_webhook_charges(request):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def stripe_webhook_invoices(request):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def stripe_webhook_plans(request):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def stripe_webhook_prices(request):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
@stripe_secure(os.getenv('DJANGO_STRIPE_WEBHOOK_SECRET_CUSTOMERS'))
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
def stripe_webhook_customer_sources(request):
    return HttpResponse(status=200)
