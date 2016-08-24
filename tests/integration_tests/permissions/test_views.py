from unittest import TestCase

from django.conf import settings
from django.shortcuts import reverse
from rest_framework.test import APIClient
from urllib.parse import urlparse, parse_qs

from alexandria_server.permissions.models import OauthToken


class GitHubAuthorizeTestCase(TestCase):

    def setUp(self):

        self.client = APIClient()

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
