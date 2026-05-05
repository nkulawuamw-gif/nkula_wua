from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.is_active:
            if hasattr(request.user, 'userprofile'):
                profile = request.user.userprofile
                profile.last_activity = timezone.now()
                profile.save(update_fields=['last_activity'])
        return None