import os

base_url = os.getenv('DJANGO_STRIPE_BASE_URL')

WEBHOOKS = [
    {
        'url': f'{ base_url }stripe_webhook/payment_ok',
        'enabled_events': [
            'invoice.payment_succeeded',
        ],
    },
    {
        'url': f'{ base_url }stripe_webhook/payment_fail',
        'enabled_events': [
            'invoice.payment_failed',
        ],
    },
    {
        'url': f'{ base_url }stripe_webhook/charges',
        'enabled_events': [
            'charge.captured',
            'charge.expired',
            'charge.failed',
            'charge.pending',
            'charge.refunded',
            'charge.succeeded',
            'charge.updated',
            'charge.dispute.closed',
            'charge.dispute.created',
            'charge.dispute.funds_reinstated',
            'charge.dispute.funds_withdrawn',
            'charge.dispute.updated',
            'charge.refund.updated',
        ],
    },
    {
        'url': f'{ base_url }stripe_webhook/invoices',
        'enabled_events': [
            'invoiceitem.created',
            'invoiceitem.deleted',
            'invoiceitem.updated',
            'invoice.created',
            'invoice.deleted',
            'invoice.finalized',
            'invoice.marked_uncollectible',
            'invoice.paid',
            'invoice.payment_action_required',
            'invoice.sent',
            'invoice.upcoming',
            'invoice.updated',
            'invoice.voided',
        ],
    },
    {
        'url': f'{ base_url }stripe_webhook/plans',
        'enabled_events': [
            'plan.created',
            'plan.deleted',
            'plan.updated',
        ],
    },
    {
        'url': f'{ base_url }stripe_webhook/prices',
        'enabled_events': [
            'price.created',
            'price.deleted',
            'price.updated',
            'product.created',
            'product.deleted',
            'product.updated',
        ],
    },
    {
        'url': f'{ base_url }stripe_webhook/customers',
        'enabled_events': [
            'customer.created',
            'customer.deleted',
            'customer.updated',
            'customer.discount.created',
            'customer.discount.deleted',
            'customer.discount.updated',
            'customer.subscription.created',
            'customer.subscription.deleted',
            'customer.subscription.pending_update_applied',
            'customer.subscription.pending_update_expired',
            'customer.subscription.trial_will_end',
            'customer.subscription.updated',
            'customer.tax_id.created',
            'customer.tax_id.deleted',
            'customer.tax_id.updated',
        ],
    },
    {
        'url': f'{ base_url }stripe_webhook/customer_sources',
        'enabled_events': [
            'customer.source.updated',
            'customer.source.expiring',
            'customer.source.deleted',
            'customer.source.created',
        ],
    },
]
