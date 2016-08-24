from django.conf import settings

import requests


def get_user_repos(user):

    repos_url = settings.GITHUB_API_URL + 'user/repos'

    headers = {'Authorization': 'token {}'.format(user.token.token)}

    response = requests.get(repos_url, headers=headers)
    response.raise_for_status()

    return response.json()
