from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from crossbox.views import (
    ReservationView,
    SessionTemplateView,
    reservation_create,
    reservation_delete,
    session_template_create,
    session_template_delete,
    generate_sessions,
    user_create,
    get_is_too_late,
)


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    url(r'^user_create/', user_create, name='user-create'),
    url(
        r'^reservation/',
        ReservationView.as_view(),
        name='reservation'
    ),
    url(
        r'^reservation_create/',
        reservation_create,
        name='reservation-create'
    ),
    url(
        r'^reservation_delete/',
        reservation_delete,
        name='reservation-delete'
    ),
    url(
        r'^session_template/',
        SessionTemplateView.as_view(),
        name='session-template'
    ),
    url(
        r'^session_template_create/',
        session_template_create,
        name='session-template-create'
    ),
    url(
        r'^session_template_delete/',
        session_template_delete,
        name='session-template-delete'
    ),
    url(
        r'^generate_sessions/',
        generate_sessions,
        name='generate-sessions',
    ),
    url(
        r'^get_is_too_late/',
        get_is_too_late,
        name='get-is-too-late',
    ),
]
