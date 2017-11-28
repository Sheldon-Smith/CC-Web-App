from django.shortcuts import render

from teams.models import Team


def list_teams(request):
    teams = Team.objects.all()
    return render(request, 'list_teams.html', {'teams': teams})


def view_team(request, name):
    team = Team.objects.get_object_or_404(name=name)
    return render(request, 'view_team.html', {'team': team})
