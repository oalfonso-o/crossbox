from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def process_request(self, request):
        path = request.path_info.lstrip('/')
        if not request.user.is_authenticated:
            if path != '' and path != 'user_create/':
                return HttpResponseRedirect(settings.LOGIN_URL)
        elif path == '':
            return HttpResponseRedirect('/reservation')
