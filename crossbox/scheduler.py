import schedule
import datetime
import time
import os
import sys
import logging
import calendar
import django
from dotenv import find_dotenv, load_dotenv

ENVIRONMENT_FILE = os.getenv('DJANGO_ENV_FILE', find_dotenv())
load_dotenv(ENVIRONMENT_FILE)

django.setup()
from crossbox.models.subscriber import Subscriber  # noqa e402


def job_name(name):
    def decorator(f):
        f.__name__ = name
        return f
    return decorator


def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))


sys.excepthook = my_handler


def today_is_last_day_of_month():
    today = datetime.date.today()
    last_day_current_month = calendar.monthrange(today.year, today.month)[1]
    return today.day == last_day_current_month


@job_name('reset_wods')
def reset_wods():
    logger.info('Reset wods to everyone when last day of month at 21:00')
    if today_is_last_day_of_month():
        logger.info('It\'s last day of month at 22:00 UTC. Reseting wods...')
        Subscriber.objects.all().update(wods=0)
        logger.info('Wods reseted.')
    else:
        logger.info('It\'s not the last day of month, skip.')


schedule.every().day.at("21:00").do(reset_wods)


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
