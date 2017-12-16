import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from account.models import User
from game.models import Team, Game, Season


def view_team(request, name):
    team = get_object_or_404(Team, name=name)
    return render(request, 'game/view_team.html', {'team': team})


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
    model = Team
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
