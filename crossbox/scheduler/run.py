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
        logger.info(
            'It\'s last day of month at 22:00 CEST. Reseting wods and paying.')
        for sub in Subscriber.objects.all():
            if sub.user.is_active:
                logger.info(f'START PROCESSING {sub}')
                receivers = [
                    sub.user.email,
                    settings.SMTP_ADMIN_NOTIFICATIONS,
                    settings.SMTP_BOSS_NOTIFICATIONS,
                ]
                sub.wods = 0
                sub.save()
                if sub.fee:
                    sub.stripe_next_payment_timestamp = (
                        get_stripe_next_payment_timestamp())
                    if not sub.fee.active:
                        sub.fee = None
                        sub.save()
                        logger.info(
                            f'END PROCESSING {sub} - Fee {sub.fee} not active')
                        continue
                    charge_description = (
                        f'sub {sub}, price {sub.fee.price_cents} '
                        f'{datetime.datetime.now()}')
                    try:
                        stripe.Charge.create(
                            amount=sub.fee.price_cents,
                            currency="eur",
                            customer=sub.stripe_customer_id,
                            description=charge_description,
                        )
                    except Exception:
                        logger.exception(
                            f'END PROCESSING {sub} - Error: Payment declined',
                            exc_info=1,
                        )
                        mail_msg = payment_failed_message(
                            receivers, sub.user.username)
                        send_mail(mail_msg, receivers)
                        continue
                    sub.stripe_last_payment_timestamp = (
                        datetime.datetime.now().timestamp())
                    sub.wods = sub.fee.num_sessions
                    sub.save()
                    mail_msg = payment_succeeded_message(
                        sub.fee, receivers, sub.user.username)
                    logger.info(
                        f'END PROCESSING {sub} - Payment correct for sub {sub} '  # noqa
                        f'{sub.wods} wods for {sub.fee.price_cents/100}€'
                    )
                    send_mail(mail_msg, receivers)
                    # avoid gmail block by spam
                    time.sleep(SECONDS_BETWEEN_MAILS)
                else:
                    logger.info(f'END PROCESSING {sub} - No payment for sub {sub}')  # noqa
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
