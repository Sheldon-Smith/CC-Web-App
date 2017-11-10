from django.db import models

from users.models import UserProfile


class Team(models.Model):

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    captain = models.ForeignKey(UserProfile, related_name='captain')
    keeper = models.ForeignKey(UserProfile, related_name='keeper')
