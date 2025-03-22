from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

class LoginRequiredMiddleware:
    """
    Middleware that ensures all views are accessed by authenticated users only,
    unless they are in the `LOGIN_EXEMPT_URLS`.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            settings.LOGIN_URL.lstrip('/'),
            'accounts/password_reset/',
            'accounts/password_reset/done/',
        ]

    def __call__(self, request):
        # Resolve the current URL name
        current_url_name = resolve(request.path_info).url_name  # noqa: F841

        # If the user is not authenticated and the URL is not exempt, redirect to login
        if not request.user.is_authenticated and request.path_info.lstrip('/') not in self.exempt_urls:
            return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response