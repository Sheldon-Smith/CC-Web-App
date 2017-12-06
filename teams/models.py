from django.db import models


class Team(models.Model):

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
