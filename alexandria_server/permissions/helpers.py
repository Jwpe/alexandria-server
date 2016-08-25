from django.conf import settings

import requests


def get_access_token(code):
    """
    Exchange a temporary code and application credentials for a GitHub OAuth
    token.
    """
    uri = settings.GITHUB_OAUTH_URL + "access_token"
    params = {
        'code': code,
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
    }
    headers = {'Accept': 'application/json'}

    response = requests.post(uri, headers=headers, params=params)
    response.raise_for_status()

    return response.json()


def get_user_from_token(token):
    """
    Get user details from the GitHub API using a valid access token.
    """
    user_url = settings.GITHUB_API_URL + 'user'
    headers = {'Authorization': 'token {}'.format(token.token)}

    response = requests.get(user_url, headers=headers)

    return response.json()
