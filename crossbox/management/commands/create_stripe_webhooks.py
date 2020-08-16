import stripe

from django.core.management.base import BaseCommand

from crossbox.management.commands.webhooks import WEBHOOKS


class Command(BaseCommand):
    help = 'Creates stripes webhooks'

    def handle(self, *args, **options):
        for webhook in WEBHOOKS:
            stripe.WebhookEndpoint.create(
                url=webhook['url'],
                enabled_events=webhook['enabled_events'],
            )
            self.stdout.write(f'Webhook {webhook["url"]} created')
        self.stdout.write(self.style.SUCCESS('Webhooks created'))
