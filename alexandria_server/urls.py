from django.conf.urls import include, url

urlpatterns = [
    url(r'^oauth/', include('alexandria_server.permissions.urls', namespace='oauth'))
]