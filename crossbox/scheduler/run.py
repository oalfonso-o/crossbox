import schedule
import datetime
import stripe
import time
import os
import sys
import logging
import django
from dotenv import find_dotenv, load_dotenv

from crossbox.scheduler.helpers import (
    today_is_last_day_of_month,
    payment_succeeded_message,
    payment_failed_message,
    send_mail,
    get_stripe_next_payment_timestamp,
)

ENVIRONMENT_FILE = os.getenv('DJANGO_ENV_FILE', find_dotenv())
load_dotenv(ENVIRONMENT_FILE)

SECONDS_BETWEEN_MAILS = 90

django.setup()
from django.conf import settings  # noqa e402
from crossbox.models.subscriber import Subscriber  # noqa e402
from crossbox.models.payment import Payment  # noqa e402


def job_name(name):
    def decorator(f):
        f.__name__ = name
        return f
    return decorator


def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))


sys.excepthook = my_handler


@job_name('pay_subscriptions')
def pay_subscriptions():
    logger.info(
        'Pay subscriptions and give wods when last day of month at 22:00')
    if today_is_last_day_of_month():
        total_subs = 0
        subs_active = 0
        subs_active_with_fee = 0
        subs_active_with_fee_inactive = 0
        stripe_errors = 0
        stripe_payments = 0
        logger.info(
            'It\'s last day of month at 22:00 CET. Reseting wods and paying.')
        for sub in Subscriber.objects.all():
            total_subs += 1
            if sub.user.is_active:
                subs_active += 1
                logger.info(f'START PROCESSING {sub}')
                receivers = [
                    sub.user.email,
                    settings.SMTP_ADMIN_NOTIFICATIONS,
                    settings.SMTP_BOSS_NOTIFICATIONS,
                ]
                sub.wods = 0
                sub.save()
                if sub.fee:
                    subs_active_with_fee += 1
                    now = datetime.datetime.now()
                    payment = Payment(
                        subscriber=sub,
                        fee=sub.fee,
                        datetime=now,
                        payed_amount=0,
                        wods=0,
                    )
                    sub.stripe_next_payment_timestamp = (
                        get_stripe_next_payment_timestamp())
                    if not sub.fee.active:
                        subs_active_with_fee_inactive += 1
                        sub.fee = None
                        sub.save()
                        payment.save()
                        logger.info(
                            f'END PROCESSING {sub} - Fee {sub.fee} not active')
                        continue
                    charge_description = (
                        f'sub {sub}, price {sub.fee.price_cents} {now}')
                    try:
                        stripe.Charge.create(
                            amount=sub.fee.price_cents,
                            currency="eur",
                            customer=sub.stripe_customer_id,
                            description=charge_description,
                        )
                    except Exception:
                        stripe_errors += 1
                        payment.stripe_error = True
                        payment.save()
                        logger.exception(
                            f'END PROCESSING {sub} - Error: Payment declined',
                            exc_info=1,
                        )
                        mail_msg = payment_failed_message(
                            receivers, sub.user.username)
                        send_mail(mail_msg, receivers)
                        continue
                    sub.stripe_last_payment_timestamp = now.timestamp()
                    sub.wods = sub.fee.num_sessions
                    payment.wods = sub.wods
                    payment.payed_amount = sub.fee.price_cents
                    sub.save()
                    payment.save()
                    mail_msg = payment_succeeded_message(
                        sub.fee, receivers, sub.user.username)
                    logger.info(
                        f'END PROCESSING {sub} - Payment correct for sub {sub} '  # noqa
                        f'{sub.wods} wods for {sub.fee.price_cents/100}€'
                    )
                    send_mail(mail_msg, receivers)
                    # avoid gmail block due to spam
                    time.sleep(SECONDS_BETWEEN_MAILS)
                    stripe_payments += 1
                else:
                    logger.info(f'END PROCESSING {sub} - No payment for sub {sub}')  # noqa
        logger.info('All payments processed! Stats:')
        logger.info(f'\t\ttotal_subs: {total_subs}')
        logger.info(f'\t\tsubs_active: {subs_active}')
        logger.info(f'\t\tsubs_active_with_fee: {subs_active_with_fee}')
        logger.info(f'\t\tsubs_active_with_fee_inactive: {subs_active_with_fee_inactive}')  # noqa
        logger.info(f'\t\tstripe_errors: {stripe_errors}')
        logger.info(f'\t\tstripe_payments: {stripe_payments}')
    else:
        logger.info('It\'s not the last day of month, skip.')


schedule.every().day.at("22:00").do(pay_subscriptions)


def run():
    logger.info('Scheduler started')
    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    log_scheduler_log_filepath = os.getenv(
        'DJANGO_SCHEDULER_LOG_FILEPATH',
        '/var/log/django/crossbox_scheduler.log')
    logging.basicConfig(
        filename=log_scheduler_log_filepath,
        level=logging.INFO,
        format=('[%(levelname)s] %(asctime)s %(message)s'),
    )
    logger = logging.getLogger(__name__)
    run()
