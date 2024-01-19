from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed

from user.models import User


class AppAuthenticationBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        password = kwargs.get('password')
        otp = kwargs.get('otp')
        email = kwargs.get('email')
        if email is None:
            email = kwargs.get('username')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user is not None:
            # Login with OTP
            if otp is not None:
                if cache.get(email) == otp:
                    return user
                raise AuthenticationFailed({'message': 'OTP không khớp'})
            # Login with password (or Admin login)
            if password is not None:
                if user.check_password(password):
                    return user
                if user.is_superuser:
                    return None
                raise AuthenticationFailed({'message': 'Password không đúng'})
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
