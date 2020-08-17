WEEK_DAYS = 7
MIDWEEK_DAYS = 5
SATURDAY_WEEK_DAY = 6
SATURDAY_TIMEDELTA_DAYS = 5
SIMPLE_TIME_POS = 5
DEFAULT_LAST_SESSION_HOUR = 13
NUM_WEEKS_IN_A_YEAR = 52

WEBHOOKS = [
    {
        'endpoint': 'stripe_webhook/payment_ok',
        'route_name': 'stripe_webhook_payment_ok',
        'enabled_events': [
            'invoice.payment_succeeded',
        ],
    },
    {
        'endpoint': 'stripe_webhook/payment_fail',
        'route_name': 'stripe_webhook_payment_fail',
        'enabled_events': [
            'invoice.payment_failed',
        ],
    },
    {
        'endpoint': 'stripe_webhook/charges',
        'route_name': 'stripe_webhook_charges',
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
        'endpoint': 'stripe_webhook/invoices',
        'route_name': 'stripe_webhook_invoices',
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
        'endpoint': 'stripe_webhook/plans',
        'route_name': 'stripe_webhook_plans',
        'enabled_events': [
            'plan.created',
            'plan.deleted',
            'plan.updated',
        ],
    },
    {
        'endpoint': 'stripe_webhook/prices',
        'route_name': 'stripe_webhook_prices',
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
        'endpoint': 'stripe_webhook/customers',
        'route_name': 'stripe_webhook_customers',
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
        'endpoint': 'stripe_webhook/customer_sources',
        'route_name': 'stripe_webhook_customer_sources',
        'enabled_events': [
            'customer.source.updated',
            'customer.source.expiring',
            'customer.source.deleted',
            'customer.source.created',
        ],
    },
]
