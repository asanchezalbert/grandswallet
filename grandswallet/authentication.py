from django.conf import settings
from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication


class TokenAuthentication(BaseTokenAuthentication):

    def __init__(self, *args, **kwargs):

        if not hasattr(settings, 'AUTH_TOKEN_MODEL'):
            raise ImproperlyConfigured(
                'To use this authentication backend '
                'you must set AUTH_TOKEN_MODEL setting')

        super(TokenAuthentication, self).__init__(*args, **kwargs)

    def get_model(self):
        return import_string(settings.AUTH_TOKEN_MODEL)

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        if not token.user.is_verified:
            raise exceptions.AuthenticationFailed('User not verified')

        return (token.user, token)


class TokenVerificationAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (token.user, token)


class TokenDocumentsAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_verified:
            raise exceptions.AuthenticationFailed('User not verified')

        return (token.user, token)
