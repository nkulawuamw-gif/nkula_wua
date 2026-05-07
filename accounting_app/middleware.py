from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from accounting_app.models import LoginSession


class SessionTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.session.session_key:
            LoginSession.objects.filter(
                session_key=request.session.session_key,
                is_active=True
            ).update(
                user=request.user
            )
        return None


class AdminAccessRestrictionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return None
                if hasattr(request.user, 'userprofile'):
                    if request.user.userprofile.role in ('admin', 'manager'):
                        return None
                logout(request)
                messages.error(request, "Access denied. Only administrators can access the admin portal.")
                return redirect('login')
            return redirect('login')
        return None


class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.is_active:
            if hasattr(request.user, 'userprofile'):
                profile = request.user.userprofile
                profile.last_activity = timezone.now()
                profile.save(update_fields=['last_activity'])
        return None