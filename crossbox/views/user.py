from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.conf import settings

from crossbox.forms import UserForm
from crossbox.views.stripe_webhooks import send_mail


def get_mail_msg(user):
    message = MIMEMultipart('alternative')
    message['Subject'] = f'Bienvenido a Crossbox {user.first_name}!'
    message['From'] = settings.SMTP_USER_NOTIFICATIONS
    message['To'] = user.email
    html = f'''\
<html>
    <body>
        <p>Hola {user.first_name} {user.last_name}</p>
        <br>
        Gracias por registrarte en Crossbox, de momento tu usuario permanece
        <b>desactivado</b> por lo que aún no podrás acceder a la aplicación
        pero en breves nos pondremos en contacto contigo para confirmar el
        alta.
        <br>
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


def send_email(user):
    msg = get_mail_msg(user)
    receivers = [
        user.email,
        settings.SMTP_ADMIN_NOTIFICATIONS,
        settings.SMTP_BOSS_NOTIFICATIONS,
    ]
    send_mail(msg, receivers)


@require_http_methods(["GET", "POST"])
def user_create(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                clean_password = form.cleaned_data['password1']
                validate_password(clean_password)
                password = make_password(clean_password, None, 'bcrypt_sha256')
                user = form.save()
                user.password = password
                user.is_active = False  # user is activated manually by admin
                user.save()
                send_email(user)
                return redirect('login')
            except ValidationError:
                form.errors['password'] = (
                    'La contraseña ha de tener mínimo 4 caracteres')
                return render(request, 'user_create.html', {'form': form})
    return render(request, 'user_create.html', {'form': form})
