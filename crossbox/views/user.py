import stripe

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.decorators.http import (
    require_GET,
    require_POST,
    require_http_methods,
)

from crossbox.forms import UserForm
from crossbox.models.card import Card


@require_http_methods(["GET", "POST"])
def user_create(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                clean_password = form.cleaned_data['password1']
                validate_password(clean_password)
                password = make_password(clean_password, None, 'bcrypt_sha256')
                user = form.save()
                user.password = password
                user.save()
            except ValidationError:
                form.errors['password'] = (
                    'La contraseña ha de tener mínimo 4 caracteres')
                return render(request, 'user_create.html', {'form': form})
            return redirect('login')
    return render(request, 'user_create.html', {'form': form})


@require_GET
def profile(request):
    user_cards = Card.objects.filter(subscriber=request.user.subscriber)
    return render(request, 'profile.html', {'user_cards': []})


@require_POST
def add_payment_method(request):
    import pudb; pudb.set_trace()
    card_token = request.POST['stripeToken']
    stripe_card = stripe.Customer.create_source(
        request.user.subscriber.stripe_customer_id,
        source=card_token,
    )
    Card.objects.create(
        last_digits=stripe_card['last4'],
        active=True,
        subscriber=request.user.subscriber,
        stripe_card_id=stripe_card['id'],
    )
    return profile(request)
