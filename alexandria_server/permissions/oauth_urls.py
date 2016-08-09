from django.conf.urls import url

from .views import GitHubAuthorize, GitHubCallback

urlpatterns = [
    url(r'^authorize/', GitHubAuthorize.as_view(), name='authorize'),
    url(r'^callback/', GitHubCallback.as_view(), name='callback'),
]
