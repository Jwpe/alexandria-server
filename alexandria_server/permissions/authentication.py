from django.conf import settings
from django.utils import timezone

from rest_framework import authentication
from rest_framework import exceptions

import datetime
import jwt

from .models import User


def generate_jwt(user):

    payload = {
        'user': user.pk,
        'exp': timezone.now() + datetime.timedelta(weeks=2),
        'iat': timezone.now()
    }
    return jwt.encode(payload, settings.SECRET_KEY)


def decode_jwt(token):

    return jwt.decode(token, settings.SECRET_KEY)


class JWTAuthentication(authentication.BaseAuthentication):

        def authenticate(self, request):

            token = self._get_jwt_from_header(request)

            try:
                payload = decode_jwt(token)
            except jwt.ExpiredSignature:
                detail = 'Signature has expired.'
                raise exceptions.AuthenticationFailed(detail=detail)
            except jwt.DecodeError:
                detail = 'Error decoding token.'
                raise exceptions.AuthenticationFailed(detail=detail)
            except jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed()

            user = self._get_user_by_id(payload)

            return (user, token)

        def _get_jwt_from_header(self, request):

            auth_header = authentication.get_authorization_header(request)

            if not auth_header:

                detail = 'No Authorization header present.'
                raise exceptions.AuthenticationFailed(detail=detail)

            try:
                prefix, token = auth_header.split()
            except ValueError:
                detail = 'Invalid Authorization header.'
                raise exceptions.AuthenticationFailed(detail=detail)

            return token

        def _get_user_by_id(self, payload):

            user_pk = payload['user']

            try:
                return User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                detail = 'Invalid payload.'
                raise exceptions.AuthenticationFailed(detail=detail)
