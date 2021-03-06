from django.conf import settings
from django.shortcuts import get_object_or_404, reverse

import json
import requests

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .authentication import generate_jwt, JWTAuthentication
from .helpers import get_access_token, get_user_from_token
from .models import OauthToken, User
from .serializers import UserSerializer


class GitHubAuthorize(APIView):

    def get(self, request):

        # build an empty OauthToken
        desired_scopes = [
            'user:email',
            'write:repo_hook',
            'public_repo'
        ]

        token = OauthToken.objects.create(scopes=desired_scopes)

        # construct oauth URL for GitHub
        oauth_url = self._get_oauth_url(request, token)

        data = {'oauth_url': oauth_url}

        return Response({'data': data})

    def _get_oauth_url(self, request, token):

        redirect_uri = request.build_absolute_uri(
            reverse('callback'))

        params = {
            'state': token.state,
            'client_id': settings.GITHUB_CLIENT_ID,
            'scope': ' '.join(token.scopes),
            'redirect_uri': redirect_uri,
        }

        uri = settings.GITHUB_OAUTH_URL + "authorize"

        oauth_url = self._add_params(uri, params)
        return oauth_url

    def _add_params(self, uri, params):
        uri_with_params = uri + '?' + '&'.join(
            ['{0}={1}'.format(k, v) for k, v in params.items()])
        return uri_with_params


class GitHubCallback(APIView):

    def get(self, request):

        state = request.query_params.get('state')
        code = request.query_params.get('code')

        # Check that this is a legitimate callback for a request made from the site
        token = get_object_or_404(OauthToken, state=state)

        try:
            data = get_access_token(code)
        except requests.HTTPError as e:
            return self._generate_error_response(e)

        if set(token.scopes) == set(data['scope'].split(',')):
            token.token = data.get('access_token')
            token.save()

            user = self._get_or_create_user(token=token)

            jwt = generate_jwt(user)
            data = {'token': jwt}

            return Response({'data': data})

        else:
            return Response({'errors': [
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'detail': "User has not authorized the correct scopes"
                }
            ]}, status=status.HTTP_403_FORBIDDEN)

    def _get_or_create_user(self, token):

        data = get_user_from_token(token.token)

        try:

            user = User.objects.get(
                github_username=data['login'], github_id=data['id'])
            user.email = data['email']

            old_token = user.token
            user.token = token
            user.save()
            old_token.delete()

        except User.DoesNotExist:

            user = User.objects.create(
                github_username=data['login'], github_id=data['id'],
                email=data['email'], token=token)

        return user

    def _generate_error_response(self, error):

        try:
            detail = error.response.json()['error']
        except json.decoder.JSONDecodeError:
            detail = "No error specified"

        return Response({
            'errors': [
                {
                    'status': error.response.status_code,
                    'detail': detail
                }
            ]
        }, status=error.response.status_code)


class UserViewset(ModelViewSet):

    queryset = User.objects.all()

    authentication_classes = (JWTAuthentication,)
    serializer_class = UserSerializer
