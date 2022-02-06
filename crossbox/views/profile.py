import stripe

from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from crossbox.models.card import Card
from crossbox.models.fee import Fee
from crossbox.models.payment import Payment


@require_GET
def profile(request):
    subscriber = request.user.subscriber
    user_cards = Card.objects.filter(subscriber=subscriber)
    last_payment = Payment.objects.filter(
        subscriber=subscriber,
    ).order_by('-datetime').first()
    if (
        last_payment
        and last_payment.payed_amount
        and last_payment.fee.morning
    ):
        user_has_morning_fee = True
    else:
        user_has_morning_fee = False
    fees = []
    fees_morning = []
    if not subscriber.fee:
        empty_fee_option = {'': {'selected': False, 'label': 'Sin cuota'}}
        fees = [empty_fee_option]
        fees_morning = [empty_fee_option]
    fee_objs = list(Fee.objects.filter(active=True).order_by('num_sessions'))
    if subscriber.fee and not subscriber.fee.active:
        fee_objs.append(subscriber.fee)
    for fee in fee_objs:
        selected = (
            bool(subscriber.fee.pk == fee.pk)
            if subscriber.fee
            else False
        )
        select_option = {'selected': selected, 'label': fee.label}
        if fee.morning:
            fees_morning.append({fee.pk: select_option})
        else:
            fees.append({fee.pk: select_option})
    return render(
        request,
        'profile.html',
        {
            'user': request.user,
            'user_cards': user_cards,
            'fees': fees,
            'fees_morning': fees_morning,
            'user_has_morning_fee': user_has_morning_fee,
            'subscriber_fee_active': (
                subscriber.fee.active if subscriber.fee else False),
        },
    )


@require_POST
def change_fee(request):
    subscriber = request.user.subscriber
    previous_fee = subscriber.fee
    morning_selected = request.POST['fee_morning_checkbox']
    if morning_selected:
        new_fee_pk = request.POST['fee_morning']
    else:
        new_fee_pk = request.POST['fee']
    new_fee = (
        Fee.objects.get(pk=new_fee_pk)
        if new_fee_pk
        else None
    )
    if previous_fee == new_fee:
        return redirect('profile')
    subscriber.fee = new_fee
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
    stripe_card_id = request.POST['stripe_card_id']
    card_to_delete = Card.objects.filter(stripe_card_id=stripe_card_id).first()
    if card_to_delete.default:
        return redirect('profile')
    subscriber = request.user.subscriber
    stripe.Customer.delete_source(
        subscriber.stripe_customer_id,
        stripe_card_id,
    )
    card_to_delete.delete()
    return redirect('profile')
