from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from crossbox.forms import UserForm


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
                user.save()
            except ValidationError:
                form.errors['password'] = (
                    'La contraseña ha de tener mínimo 4 caracteres')
                return render(request, 'user_create.html', {'form': form})
            return redirect('login')
    return render(request, 'user_create.html', {'form': form})


def profile(request):
    return render(request, 'profile.html',)
