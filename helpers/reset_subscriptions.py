import stripe
import datetime
from dateutil.relativedelta import relativedelta

from crossbox.models.subscriber import Subscriber


def get_next_billing_cycle_anchor():
    today = datetime.datetime.today()
    first_day = today.replace(day=1) + relativedelta(months=1)
    first_day_wo_time = first_day.replace(
        hour=0, minute=0, second=0, microsecond=0)
    return int(first_day_wo_time.timestamp())


def reset_subscriptions(subscriptions):
    for sub in subscriptions['data']:
        customer_id = sub['customer']
        print("customer: " + customer_id)
        django_subscriber = Subscriber.objects.get(
            stripe_customer_id=customer_id)
        if django_subscriber.fee:
            stripe.Subscription.delete(
                django_subscriber.stripe_subscription_id)
            stripe_subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": django_subscriber.fee.stripe_price_id}],
                proration_behavior='none',
                billing_cycle_anchor=get_next_billing_cycle_anchor(),
            )
            django_subscriber.stripe_subscription_id = (
                stripe_subscription['id'])
            django_subscriber.stripe_next_payment_timestamp = (
                stripe_subscription['current_period_end']
            django_subscriber.stripe_subscription_price_item_id = (
                stripe_subscription['items']['data'][0].id
            )
            django_subscriber.save()


if __name__ == '__main__':
    # Ideally to be used with django shell
    # use starting_after='sub_IDxxx' for more than 100 subs
    subscriptions = stripe.Subscription.list(limit=100)
    reset_subscriptions(subscriptions)
