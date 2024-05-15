# backend/authentication.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Profile

class FullNameMobileNumberBackend(BaseBackend):
    def authenticate(self, request, full_name=None, mobile_number=None, **kwargs):
        try:
            profile = Profile.objects.get(full_name=full_name, mobile_number=mobile_number)
            return profile.user
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
