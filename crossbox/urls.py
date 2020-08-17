from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from crossbox.constants import WEBHOOKS
from crossbox.views.session import generate_sessions, change_session_type
from crossbox.views.user import user_create
from crossbox.views.profile import (
    profile,
    change_fee,
    add_payment_method,
    set_default_payment_method,
    delete_card,
)
from crossbox.views.reservation import (
    ReservationView,
    reservation_create,
    reservation_delete,
)
from crossbox.views.session_template import (
    SessionTemplateView,
    session_template_create,
    session_template_delete,
    session_template_switch,
)
from crossbox.views.stripe_webhooks import STRIPE_WEBHOOKS_VIEWS_MAPPER

webhook_paths = [
    path(
        webhook['endpoint'],
        STRIPE_WEBHOOKS_VIEWS_MAPPER[webhook['route_name']],
        name=webhook['route_name'],
    )
    for webhook in WEBHOOKS
]

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    url(r'^user_create/', user_create, name='user-create'),
    url(r'^profile/', profile, name='profile'),
    url(r'^change_fee/', change_fee, name='change_fee'),
    url(
        r'^add_payment_method/',
        add_payment_method,
        name='add_payment_method',
    ),
    url(
        r'^set_default_payment_method/',
        set_default_payment_method,
        name='set_default_payment_method',
    ),
    url(r'^delete_card/', delete_card, name='delete_card'),
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
        r'^session_template_switch/',
        session_template_switch,
        name='session-template-switch'
    ),
    url(
        r'^generate_sessions/',
        generate_sessions,
        name='generate-sessions',
    ),
    path(
        'change_session_type/<int:session_id>/',
        change_session_type,
        name='change_session_type',
    ),
    *webhook_paths,
]
