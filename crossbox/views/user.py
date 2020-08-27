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
    message['Subject'] = f'Bienvenido a Crossbox {user.username}!'
    message['From'] = settings.SMTP_USER_NOTIFICATIONS
    message['To'] = user.email
    html = f'''\
<html>
    <body>
        <p>Hola {user.first_name} {user.last_name},</p>
        <br>
        Gracias por registrarte en Crossbox, todavía no hemos activado tu
        usuario por lo que aún no podrás acceder a la aplicación
        pero en breves lo activaremos. En cuanto lo hagamos recibirás un mail
        de notifiación.
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


def send_new_user_email(user):
    msg = get_mail_msg(user)
    receivers = [user.email]
    send_mail(msg, receivers)


def get_mail_admin_msg(user):
    message = MIMEMultipart('alternative')
    message['Subject'] = f'Nuevo usuario {user.username}! Actívalo!'
    message['From'] = settings.SMTP_USER_NOTIFICATIONS
    message['To'] = user.email
    html = f'''\
<html>
    <body>
        <p>Hola admin, {user.first_name} {user.last_name} se ha registrado,</p>
        <br>
        Para activar este usuario:
        <a href="{settings.BASE_URL}/admin/auth/user/{user.pk}/change/#/tab/module_2/">
        Ir a su perfil</a>.
        <br>
        <br>
        <br>
        Atentamente,
        <br>
        El equipo de <a href="https://www.crossboxpalau.com/">Crossbox Palau
        </a>
    </p>
  </body>
</html>'''  # noqa
    html_part = MIMEText(html, 'html')
    message.attach(html_part)
    return message.as_string()


def send_new_user_email_admin(user):
    msg = get_mail_admin_msg(user)
    receivers = [
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
                user = form.save(commit=False)
                user.password = password
                user.is_active = False  # user is activated manually by admin
                user.save()
                send_new_user_email(user)
                send_new_user_email_admin(user)
                return redirect('login')
            except ValidationError:
                form.errors['password'] = (
                    'La contraseña ha de tener mínimo 4 caracteres')
                return render(request, 'user_create.html', {'form': form})
    return render(request, 'user_create.html', {'form': form})
