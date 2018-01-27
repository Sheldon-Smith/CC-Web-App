import datetime

from django.db import models

from account.models import User
from django.utils.translation import ugettext_lazy as _


class Season(models.Model):

    name = models.CharField(max_length=30)
    year = models.PositiveIntegerField()
    number_of_weeks = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    player = models.ForeignKey(User, related_name='team_member')
    team = models.ForeignKey('Team', related_name='team_member')
    season = models.ForeignKey('Season', related_name='team_member')

    def __unicode__(self):
        return self.player.get_full_name()

    def __str__(self):
        return self.player.get_full_name()


class Statkeeper(models.Model):
    statkeeper = models.ForeignKey(User, related_name='stat_keeper')
    team = models.ForeignKey('Team', related_name='stat_keeper')
    season = models.ForeignKey('Season', related_name='stat_keeper')

    def __unicode__(self):
        return self.statkeeper.get_full_name()

    def __str__(self):
        return self.statkeeper.get_full_name()


class TeamInfo(models.Model):

    team = models.ForeignKey('Team')
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    season = models.ForeignKey('Season')


class Team(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    captain = models.ForeignKey(User, related_name='captain', blank=True, null=True)
    keeper = models.ForeignKey(User, related_name='keeper', blank=True, null=True)
    players = models.ManyToManyField('account.User', through='TeamMember', related_name="players")
    statkeepers = models.ManyToManyField('account.User', through='Statkeeper', related_name="statkeepers" )
    division = models.CharField(max_length=4, choices=(("Pink", "Pink"), ("Blue", "Blue")), blank=True, null=True)

    def __unicode__(self):
        return self.get_name()

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return "Team %s" % self.name
    get_name.short_description = "Team Name"

    def get_statkeepers(self):
        return "\n".join([keeper.get_first_name() for keeper in self.statkeepers.all()])
    get_statkeepers.short_description = "Statkeepers"

    def can_keep_stats(self, user):
        statkeepers = [statkeeper for statkeeper in self.statkeepers.all()]
        if user == self.captain or user == self.keeper or user in statkeepers:
            return True
        return False


class Score(models.Model):

    user = models.ForeignKey(User, related_name='score')
    top_makes = models.PositiveIntegerField()
    bottom_makes = models.PositiveIntegerField()
    top_gays = models.PositiveIntegerField()
    bottom_gays = models.PositiveIntegerField()
    misses = models.PositiveIntegerField()
    date = models.DateField(_("Date"), default=datetime.date.today)
    game = models.ForeignKey('Game', related_name='score')

    def __str__(self):
        return self.user.get_full_name()

    def __unicode__(self):
        return self.user.get_full_name()

    def get_shot_percentage(self):
        total_shots = self.total_makes() + self.misses
        # TODO Avoid div by zero - probably a method that does this more elegantly
        if total_shots == 0:
            total_shots = 1
        return int(self.total_makes()/total_shots*100)

    def total_makes(self):
        return self.top_makes + self.bottom_makes + self.top_gays + self.bottom_gays


class Game(models.Model):

    home_team = models.ForeignKey(Team, related_name='home_team')
    away_team = models.ForeignKey(Team, related_name='away_team')
    home_cups = models.IntegerField(blank=True, null=True)
    away_cups = models.IntegerField(blank=True, null=True)
    winner = models.ForeignKey(Team, related_name='winner', blank=True, null=True)
    loser = models.ForeignKey(Team, related_name='loser', blank=True, null=True)
    season = models.ForeignKey(Season)
    week = models.IntegerField(blank=True, null=True)
    public = models.BooleanField(_('Public'), default=True)
    playoff = models.BooleanField(_('Playoff game'), default=False)
    played = models.BooleanField(_('Played'), default=False)
    scrimmage = models.BooleanField(_('Scrimmage'), default=False)

    def __str__(self):
        return "%s vs %s" % (self.home_team, self.away_team)

    def __unicode__(self):
        return "%s vs %s" % (self.home_team, self.away_team)
