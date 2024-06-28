from django.contrib.auth.backends import BaseBackend
from .models import *

class CustomAuthTokenBackend(BaseBackend):
    def authenticate(self, request, token=None):
        if not token:
            return None

        try:
            token_obj = AuthToken.objects.get(token=token)
        except AuthToken.DoesNotExist:
            return None

        if not token_obj.is_valid():
            return None

        return token_obj.user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
