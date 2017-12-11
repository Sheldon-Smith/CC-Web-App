import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from game.models import Team, Game, Season


def list_teams(request):
    teams = Team.objects.all()
    return render(request, 'list_teams.html', {'teams': teams})


def view_team(request, name):
    team = Team.objects.get_object_or_404(name=name)
    return render(request, 'view_team.html', {'team': team})


@login_required
def get_teams(request):
    if request.method == "GET":
        game_type = request.GET['game_type']
        if game_type == 'casual':
            return JsonResponse({'home_team_name': "Blue",
                                 'away_team_name': "Red"})
        return JsonResponse({'home_team_name': "BIG",
                             'away_team_name': "PROBLEM"})