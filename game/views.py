import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from account.models import User
from game.models import Team, Game, Season


def view_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'game/view_team.html', {'team': team})


def schedule(request):
    seasons = Season.objects.all().exclude(name='Casual')
    return render(request, 'game/schedule.html', {'seasons': seasons,
                                                  'number_of_weeks': range(1, 1 + seasons[0].number_of_weeks)})


def update_schedule(request):
    season_id = request.GET['season']
    week = request.GET['week']
    season = Season.objects.get(id=season_id)
    week_schedule = Game.objects.filter(season_id=season_id).filter(week=week)
    teams = []
    for game in week_schedule:
        teams.append({'home_team': list(Team.objects.filter(pk=game.home_team.pk).values()),
                      'away_team': list(Team.objects.filter(pk=game.away_team.pk).values())})

    return JsonResponse({'schedule': teams,
                         'weeks': list(range(1, 1 + season.number_of_weeks))})


@login_required
def get_teams(request):
    if request.method == "GET":
        game_type = request.GET['game_type']
        if game_type == 'casual':
            return JsonResponse({'home_team_name': "Blue",
                                 'away_team_name': "Red"})
        return JsonResponse({'home_team_name': "BIG",
                             'away_team_name': "PROBLEM"})


class TeamListView(ListView):
    queryset = Team.objects.exclude(name="Blue").exclude(name="Red")
    context_object_name = 'teams'
    template_name = 'game/list_teams.html'


class TeamMemberListView(ListView):

    model = Team
    context_object_name = 'teams'
    template_name = 'game/view_team.html'


class PlayerListView(ListView):
    model = User
    context_object_name = 'players'
    template_name = 'game/list_players.html'
