from django.db import models
from django.utils import timezone

from alexandria_server.permissions.models import User


class Repository(models.Model):

    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True)

    url = models.URLField(max_length=1024)
    api_url = models.URLField(max_length=1024)

    # Internal timestamp
    timestamp = models.DateTimeField(default=timezone.now)
    # GitHub-supplied timestamps
    created = models.DateTimeField()
    updated = models.DateTimeField()


class Project(models.Model):
    """
    The top-level documentation entity. Corresponds to one or many GitHub
    repositories' combined into one documentation view.
    """
    name = models.CharField(max_length=1024)
    published = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    members = models.ManyToManyField(User)

    repositories = models.ManyToManyField(Repository)
