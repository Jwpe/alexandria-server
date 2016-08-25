from unittest import TestCase, mock

from django.conf import settings
from django.shortcuts import reverse
from rest_framework.test import APIClient

import requests
from urllib.parse import urlparse, parse_qs

from alexandria_server.permissions.models import OauthToken, User


class GitHubAuthorizeTestCase(TestCase):

    def setUp(self):

        self.client = APIClient()

    def tearDown(self):

        OauthToken.objects.get().delete()

    def test_get_token(self):
        """
        Check that an empty token is correctly created when a request is made
        to the GitHubAuthorize endpoint.
        """
        response = self.client.get(reverse("authorize"))

        self.assertEqual(200, response.status_code)

        token = OauthToken.objects.get()

        url = response.data['data']['oauth_url']
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)

        # For whatever reason parse_qs returns a list for each param
        self.assertEqual(token.state, params.get('state')[0])
        self.assertEqual(settings.GITHUB_CLIENT_ID, params.get('client_id')[0])


class GitHubCallbackTestCase(TestCase):

    def setUp(self):

        self.client = APIClient()

        desired_scopes = [
            'user:email',
            'write:repo_hook',
            'public_repo'
        ]
        self.token = OauthToken.objects.create(scopes=desired_scopes)

    @mock.patch('alexandria_server.permissions.views.generate_jwt')
    @mock.patch('alexandria_server.permissions.views.get_user_from_token')
    @mock.patch('alexandria_server.permissions.views.get_access_token')
    def test_get_callback(self, mock_get_access_token, mock_get_user,
            mock_generate_jwt):
        """
        Make sure that on recieving a valid callback, a user is created and
        the OAuth token is updated with authorization credentials.
        """
        mock_get_access_token.return_value = {
            'scope': 'user:email,write:repo_hook,public_repo',
            'access_token': 'i_am_a_token'
        }

        mock_get_user.return_value = {
            'login': 'AmeliaEarheart',
            'id': '12345',
            'email': 'amelia@planes.co.uk'
        }

        mock_generate_jwt.return_value = 'hi.iama.jwt'

        params = {
            'state': self.token.state,
            'code': 'a_temporary_code'
        }

        url = reverse("callback") + "?state={state}&code={code}".format(
            **params)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        # Make sure that helper functions were called correctly
        mock_get_access_token.assert_called_once_with('a_temporary_code')

        token = OauthToken.objects.get()
        mock_get_user.assert_called_once_with(token.token)

        # Make sure a user was created
        user = User.objects.get()
        self.assertEqual('amelia@planes.co.uk', user.email)

        # Make sure a JWT is correctly returned
        self.assertEqual('hi.iama.jwt', response.data['data']['token'])

    def test_get_callback_invalid_token(self):
        """
        Test that if no token with the recieved state exists, the endpoint
        returns a 404 response.
        """
        params = {
            'state': 'an_invalid_state',
            'code': 'a_temporary_code'
        }

        url = reverse("callback") + "?state={state}&code={code}".format(
            **params)
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    @mock.patch('alexandria_server.permissions.views.get_access_token')
    def test_get_callback_incorrect_scopes(self, mock_get_access_token):
        """
        Make sure that if the user has not authorized the correct scopes,
        the endpoint returns a 403 response.
        """
        mock_get_access_token.return_value = {
            'scope': 'user:email,public_repo',
            'access_token': 'i_am_a_token'
        }

        params = {
            'state': self.token.state,
            'code': 'a_temporary_code'
        }

        url = reverse("callback") + "?state={state}&code={code}".format(
            **params)
        response = self.client.get(url)

        self.assertEqual(403, response.status_code)
        self.assertEqual("User has not authorized the correct scopes",
            response.data['errors'][0]['detail'])

    @mock.patch('alexandria_server.permissions.views.get_access_token')
    def test_get_callback_http_error(self, mock_get_access_token):
        """
        Make sure that if the call to exchange a temporary code for an access
        token fails, the endpoint returns an error.
        """
        mock_response = mock.Mock()
        mock_response.json.return_value = {'error': 'oh no!'}
        mock_response.status_code = 500

        mock_get_access_token.side_effect = requests.HTTPError(
            response=mock_response)

        params = {
            'state': self.token.state,
            'code': 'a_temporary_code'
        }

        url = reverse("callback") + "?state={state}&code={code}".format(
            **params)
        response = self.client.get(url)

        self.assertEqual(500, response.status_code)
        self.assertEqual("oh no!", response.data['errors'][0]['detail'])
