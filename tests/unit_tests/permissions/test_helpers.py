from unittest import TestCase, mock

from django.conf import settings

from requests import HTTPError

from alexandria_server.permissions.helpers import get_access_token

class HelperTestCase(TestCase):

    @mock.patch('alexandria_server.permissions.helpers.requests.post')
    def test_get_access_token(self, mock_post):
        """
        Check that get_access_token POSTs the correct data to the
        GitHub API.
        """
        mock_response = mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'access_token': 'im_a_token'}

        mock_post.return_value = mock_response

        data = get_access_token('a_code')

        expected_params = {
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'client_id': settings.GITHUB_CLIENT_ID,
            'code': 'a_code'
        }
        mock_post.assert_called_once_with(
            'https://github.com/login/oauth/access_token',
            headers={'Accept': 'application/json'},
            params=expected_params)

        self.assertEqual({'access_token': 'im_a_token'}, data)

    @mock.patch('alexandria_server.permissions.helpers.requests.post')
    def test_get_access_token_http_error(self, mock_post):
        """Check that a HTTP error is propagated."""
        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = HTTPError

        mock_post.return_value = mock_response

        with self.assertRaises(HTTPError):
            get_access_token('a_code')
