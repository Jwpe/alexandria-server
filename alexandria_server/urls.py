from django.conf.urls import url
from rest_framework import routers

from alexandria_server.permissions.views import (
    GitHubAuthorize, GitHubCallback, UserViewset)

from alexandria_server.projects.views import (
    PossibleRepositories)

urlpatterns = [
    url(r'^oauth/authorize/', GitHubAuthorize.as_view(), name='authorize'),
    url(r'^oauth/callback/', GitHubCallback.as_view(), name='callback'),
]

router = routers.SimpleRouter()
router.register(r'users', UserViewset)
urlpatterns += router.urls

urlpatterns += [
    url(r'^user/repos/possible/', PossibleRepositories.as_view(),
        name='possible_repos')
]
