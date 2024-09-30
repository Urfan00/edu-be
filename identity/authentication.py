from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import AccessToken


class ActiveTokenJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        validated_token = super().get_validated_token(raw_token)

        try:
            access_token = AccessToken.objects.get(jti=validated_token["jti"])
            if not access_token.is_active:
                raise AuthenticationFailed("Token is inactive")
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed("Token not found")

        return validated_token
