import stripe

from crossbox.models.subscriber import Subscriber


def update_subscription_items_ids():
    django_subscribers = Subscriber.objects.all()
    for django_subscriber in django_subscribers:
        customer_id = django_subscriber.stripe_customer_id
        print("customer: " + customer_id)
        sub_id = django_subscriber.stripe_subscription_id
        if sub_id:
            print("sub_id: " + sub_id)
            stripe_subscription = stripe.Subscription.retrieve(sub_id)
            si_id = stripe_subscription['items']['data'][0].id
            django_subscriber.stripe_subscription_price_item_id = si_id
            print("sub_item_id: " + sub_id)
            django_subscriber.save()


if __name__ == '__main__':
    # This main is a sample, update_subscription_items_ids has to be used with
    # django shell copying the code there to load django env
    update_subscription_items_ids()
