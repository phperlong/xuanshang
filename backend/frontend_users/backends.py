from django.contrib.auth.backends import BaseBackend
from frontend_users.models import FrontendUser

class FrontendUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = FrontendUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except FrontendUser.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return FrontendUser.objects.get(pk=user_id)
        except FrontendUser.DoesNotExist:
            return None