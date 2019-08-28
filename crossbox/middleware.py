from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than settings.NOT_LOGIN_REQUIRED_ROUTES.
    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def process_request(self, request):
        current_route_name = resolve(request.path_info).url_name
        if not request.user.is_authenticated:
            if current_route_name not in settings.NOT_LOGIN_REQUIRED_ROUTES:
                return HttpResponseRedirect(settings.LOGIN_URL)
        elif current_route_name in settings.NOT_LOGIN_REQUIRED_ROUTES:
            return HttpResponseRedirect('/reservation')
