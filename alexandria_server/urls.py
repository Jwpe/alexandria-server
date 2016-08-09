from django.conf.urls import include, url

urlpatterns = [
    url(r'^oauth/', include(
        'alexandria_server.permissions.oauth_urls', namespace='oauth')),
    url(r'^users', include(
        'alexandria_server.permissions.urls', namespace='users'))
]
