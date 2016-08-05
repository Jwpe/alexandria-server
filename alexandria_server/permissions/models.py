from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

import uuid

class OauthToken(models.Model):
    """
    Stores Ouath Credentials for contacting github.
    """
    token = models.CharField(max_length=255, blank=True, null=True)
    scopes = ArrayField(base_field=models.CharField(max_length=255))
    state = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.state = self.state or uuid.uuid4()
        super(OauthToken, self).save(*args, **kwargs)

class User(models.Model):
    """
    A basic user model that is used for authentication.
    """

    email = models.EmailField(unique=True)
    github_id = models.IntegerField()
    token = models.ForeignKey(OauthToken)

