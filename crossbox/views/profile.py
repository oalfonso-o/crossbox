import stripe
import datetime
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from crossbox.models.card import Card
from crossbox.models.fee import Fee


def get_next_billing_cycle_anchor():
    today = datetime.datetime.today()
    first_day = today.replace(day=1) + relativedelta(months=1)
    first_day_wo_time = first_day.replace(
        hour=0, minute=0, second=0, microsecond=0)
    return int(first_day_wo_time.timestamp())


@require_GET
def profile(request):
    subscriber = request.user.subscriber
    user_cards = Card.objects.filter(subscriber=subscriber)
    empty_fee_option = {'': {'selected': False, 'label': 'Sin cuota'}}
    fees = [empty_fee_option]
    for fee in Fee.objects.filter(active=True).order_by('num_sessions'):
        selected = (
            bool(subscriber.fee.pk == fee.pk)
            if subscriber.fee
            else False
        )
        select_option = {'selected': selected, 'label': fee.label}
        fees.append({fee.pk: select_option})
    return render(
        request,
        'profile.html',
        {
            'user': request.user,
            'user_cards': user_cards,
            'fees': fees,
        },
    )


@require_POST
def change_fee(request):
    subscriber = request.user.subscriber
    previous_fee = subscriber.fee
    new_fee_pk = request.POST['fee']
    buy_immediately = request.POST.get('buy_immediately')
    new_fee = (
        Fee.objects.get(pk=new_fee_pk)
        if new_fee_pk
        else None
    )
    subscriber.fee = new_fee
    if not previous_fee and new_fee:
        billing_cycle_anchor = (
            'now' if buy_immediately else get_next_billing_cycle_anchor())
        stripe_subscription = stripe.Subscription.create(
            customer=subscriber.stripe_customer_id,
            items=[{"price": subscriber.fee.stripe_price_id}],
            proration_behavior=None,
            billing_cycle_anchor=billing_cycle_anchor,
        )
        subscriber.stripe_subscription_id = stripe_subscription['id']
        subscriber.stripe_billing_cycle_anchor = stripe_subscription[
            'billing_cycle_anchor']
    elif previous_fee and new_fee:
        billing_cycle_anchor = 'now' if buy_immediately else 'unchanged'
        stripe_subscription = stripe.Subscription.modify(
            subscriber.stripe_subscription_id,
            items=[{"price": subscriber.fee.stripe_price_id}],
            billing_cycle_anchor=billing_cycle_anchor,
        )
        subscriber.stripe_billing_cycle_anchor = stripe_subscription[
            'billing_cycle_anchor']
    elif not new_fee:
        stripe.Subscription.delete(subscriber.stripe_subscription_id)
    else:
        raise Exception('Something went wrong')
    subscriber.save()
    return redirect('profile')


@require_POST
def add_payment_method(request):
    card_token = request.POST['stripeToken']
    subscriber = request.user.subscriber
    stripe_card = stripe.Customer.create_source(
        subscriber.stripe_customer_id,
        source=card_token,
    )
    default_card = not bool(Card.objects.filter(subscriber=subscriber).count())
    Card.objects.create(
        last_digits=stripe_card['last4'],
        subscriber=subscriber,
        default=default_card,  # True if is the first card, False for next ones
        stripe_card_id=stripe_card['id'],
    )
    return redirect('profile')


@require_POST
def set_default_payment_method(request):
    subscriber = request.user.subscriber
    stripe_card_id = request.POST['stripe_card_id']
    stripe.Customer.modify(
        subscriber.stripe_customer_id,
        default_source=stripe_card_id,
    )
    user_cards = Card.objects.filter(subscriber=subscriber)
    for user_card in user_cards:
        if user_card.stripe_card_id == stripe_card_id:
            new_default_card = user_card
        if user_card.default:
            user_card.default = False
            user_card.save()
    new_default_card.default = True
    new_default_card.save()
    return redirect('profile')


@require_POST
def delete_card(request):
    subscriber = request.user.subscriber
    stripe_card_id = request.POST['stripe_card_id']
    stripe.Customer.delete_source(
        subscriber.stripe_customer_id,
        stripe_card_id,
    )
    card_to_delete = Card.objects.filter(stripe_card_id=stripe_card_id).first()
    card_to_delete.delete()
    if card_to_delete.default:
        card_to_be_default = Card.objects.filter(subscriber=subscriber).first()
        if card_to_be_default:
            card_to_be_default.default = True
            card_to_be_default.save()
    return redirect('profile')
