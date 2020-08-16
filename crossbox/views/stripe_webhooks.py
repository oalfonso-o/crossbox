from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


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
def stripe_webhook_customers(request):
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def stripe_webhook_customer_sources(request):
    return HttpResponse(status=200)
