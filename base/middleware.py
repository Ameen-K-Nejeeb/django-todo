# base/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RestrictBackAfterLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of restricted pages for logged-in users
        restricted_paths = [
            reverse('login'),
            reverse('register'),
            reverse('admin-login'),
        ]

        # If user is logged in and trying to access login/register/admin-login
        if request.user.is_authenticated and request.path in restricted_paths:
            # Redirect to their respective dashboard instead
            if request.user.is_staff or request.user.is_superuser:
                return redirect('admin-dashboard')
            else:
                return redirect('tasks')

        return self.get_response(request)


class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # ✅ Paths where caching should be disabled
        no_cache_paths = [
            '/login/',
            '/register/',
            '/tasks/',                # user dashboard
            '/admin-login/',
            '/admin-dashboard/',
        ]

        # Disable cache only for specific paths
        if any(request.path.startswith(path) for path in no_cache_paths):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response

