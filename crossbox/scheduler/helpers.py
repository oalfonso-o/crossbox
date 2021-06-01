import datetime
import calendar
import logging
import ssl
import smtplib
from dateutil.relativedelta import relativedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings


def today_is_last_day_of_month():
    today = datetime.date.today()
    last_day_current_month = calendar.monthrange(today.year, today.month)[1]
    return today.day == last_day_current_month


def get_stripe_next_payment_timestamp():
    # this must be called on last day of month, before changing month
    tomorrow = datetime.datetime.today() + relativedelta(days=1)
    first_day = tomorrow.replace(day=1) + relativedelta(months=1)
    first_day_wo_time = first_day.replace(
        hour=0, minute=0, second=0, microsecond=0)
    return int(first_day_wo_time.timestamp())


def payment_succeeded_message(fee, receivers, username):
    message = MIMEMultipart('alternative')
    message['Subject'] = (
        f'{username} acabas de comprar {fee.num_sessions} wods!')
    message['From'] = settings.SMTP_USER_NOTIFICATIONS
    message['To'] = ', '.join(receivers)
    html = f'''\
<html>
    <body>
        <p>Hei, te notificamos que hemos recibido tu pago!</p>
        <p>Has comprado <b>{fee.num_sessions}</b> wods por
        <b>{fee.price_cents / 100}€</b>
        </p>
        Recuerda que siempre puedes modificar tu cuota des de tu
        <a href="{settings.BASE_URL}/profile/">perfil</a>.
        <br>
        <br>
        Muchas gracias!
        <br>
        <br>
        Atentamente,
        <br>
        El equipo de <a href="https://www.crossboxpalau.com/">Crossbox Palau
        </a>
    </p>
  </body>
</html>'''
    html_part = MIMEText(html, 'html')
    message.attach(html_part)
    return message.as_string()


def payment_failed_message(receivers, username):
    message = MIMEMultipart('alternative')
    message['Subject'] = (
        f'{username} no hemos podido procesar tu pago de Crossbox :(')
    message['From'] = settings.SMTP_USER_NOTIFICATIONS
    message['To'] = ', '.join(receivers)
    html = f'''\
<html>
    <body>
        <p>Hei, lamentablemente no hemos podido procesar el pago de tu cuota.
        </p>
        <p>Es posible que tu método de pago haya caducado o que lo hayas
        eliminado de tu perfil. Comprueba que tengas un método de pago
        válido activado en tu
        <a href="{settings.BASE_URL}/profile/">perfil</a> y
        si no recibes confirmación del pago
        en las próximas horas ponte en contacto con nosotros directamente por
        whatsapp o mandando un mail a
        <a href="{settings.SMTP_BOSS_NOTIFICATIONS}">
        {settings.SMTP_BOSS_NOTIFICATIONS}</a>.
        </p>
        <br>
        <br>
        Muchas gracias!
        <br>
        <br>
        Atentamente,
        <br>
        El equipo de <a href="https://www.crossboxpalau.com/">Crossbox Palau
        </a>
    </p>
  </body>
</html>'''
    html_part = MIMEText(html, 'html')
    message.attach(html_part)
    return message.as_string()


def send_mail(message, receivers):
    retry_count = 0
    exception = None
    while retry_count < 3:
        retry_count += 1
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(
                settings.SMTP_SERVER_NOTIFICATIONS,
                settings.SMTP_PORT_NOTIFICATIONS,
            ) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(
                    settings.SMTP_USER_NOTIFICATIONS,
                    settings.SMTP_PASSWORD_NOTIFICATIONS,
                )
                server.sendmail(
                    settings.SMTP_USER_NOTIFICATIONS, receivers, message)
                return
        except Exception as e:
            exception = str(e)
    logging.error(
        f'SMTP ERROR: Couldn\'t send to {receivers}. '
        f'Reason: {exception or ""}'
    )
