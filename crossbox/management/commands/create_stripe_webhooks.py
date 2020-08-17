import stripe

from django.core.management.base import BaseCommand
from django.conf import settings

from crossbox.constants import WEBHOOKS


class Command(BaseCommand):
    help = 'Creates stripes webhooks'

    def handle(self, *args, **options):
        base_url = settings.BASE_URL
        for webhook in WEBHOOKS:
            url = f'{base_url}/{webhook["endpoint"]}'
            stripe.WebhookEndpoint.create(
                url=url,
                enabled_events=webhook['enabled_events'],
            )
            self.stdout.write(f'Webhook {url} created')
        self.stdout.write(self.style.SUCCESS('Webhooks created'))
