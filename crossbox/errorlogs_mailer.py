import os
import subprocess
import logging
import smtplib
import ssl
import threading
from dotenv import find_dotenv, load_dotenv

ENVIRONMENT_FILE = os.getenv('DJANGO_ENV_FILE', find_dotenv())
load_dotenv(ENVIRONMENT_FILE)


MAIL_SERVER = os.getenv('DJANGO_SMTP_SERVER_NOTIFICATIONS')
MAIL_PORT = os.getenv('DJANGO_SMTP_PORT_NOTIFICATIONS')
MAIL_USER = os.getenv('DJANGO_SMTP_USER_NOTIFICATIONS')
MAIL_PASSWORD = os.getenv('DJANGO_SMTP_PASSWORD_NOTIFICATIONS')
MAIL_RECEIVERS = os.getenv('DJANGO_SMTP_ADMIN_NOTIFICATIONS')
PROJECT_ENVIRONMENT = os.getenv('DJANGO_PROJECT_ENVIRONMENT')


def mail(line):
    message = f'''\
Subject:{PROJECT_ENVIRONMENT} - Errors in CrossboxPalau APP
To:{MAIL_RECEIVERS}

Errors found:
{line}'''
    context = ssl.create_default_context()
    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(MAIL_USER, MAIL_PASSWORD)
        server.sendmail(MAIL_USER, MAIL_RECEIVERS.split(','), message)


def tail_logs(logfile):
    f = subprocess.Popen(
        ['tail', '-F', '-n1', logfile],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    while True:
        line = f.stdout.readline()
        line = line.decode('utf-8').lower()
        if 'error' in line:
            logger.info(line)
            mail(line)


if __name__ == '__main__':
    log_filepath = os.getenv(
        'DJANGO_LOG_FILEPATH', '/var/log/django/django_crossboxpalau_dev.log')
    log_scheduler_log_filepath = os.getenv(
        'DJANGO_SCHEDULER_LOG_FILEPATH',
        '/var/log/django/crossbox_scheduler.log')
    log_error_mailer_log_filepath = os.getenv(
        'DJANGO_LOG_ERROR_MAILER_LOG_FILEPATH',
        '/var/log/django/crossbox_error_mailer.log')
    logging.basicConfig(
        filename=log_error_mailer_log_filepath,
        level=logging.INFO,
        format=('[%(levelname)s] %(asctime)s %(message)s'),
    )
    logger = logging.getLogger(__name__)
    logger.info('Reading logs and email when error')
    threads = []
    try:
        t = threading.Thread(target=tail_logs, args=(log_filepath,))
        t.start()
        threads.append(t)
        t = threading.Thread(
            target=tail_logs, args=(log_scheduler_log_filepath,))
        t.start()
        threads.append(t)
    except Exception:
        for thread in threads:
            thread.join()
