import csv

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from account.models import User
from game.models import Team, Game, Season, Score


def view_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    per_dict = {}
    for player in team.players.all().order_by('first_name'):
        per_dict[player.id] = get_percentage(player)

    return render(request, 'game/view_team.html', {'team': team, 'percentages': per_dict})


def export_to_csv(request):
    pk = request.GET.get('pk', None)
    if pk:
        season = Season.objects.get(pk=pk)
    else:
        season = Season.objects.get(name='Casual')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stats.csv"'

    writer = csv.writer(response)
    writer.writerow(['Week', 'Game', 'Player', 'Top Makes', 'Top Gays', 'Bottom Makes', 'Bottom Gays',
                     'Total Makes', 'Misses', 'Shot Percentage'])
    scores = Score.objects.filter(game__season=season)
    for score in scores:
        writer.writerow([score.game.week, score.game, score.user.get_full_name(), score.top_makes, score.top_gays,
                         score.bottom_makes, score.bottom_gays, score.total_makes(), score.misses,
                         score.get_shot_percentage()])

    return response


# TODO: Should Probably be in a model
def get_percentage(player):
    percentage = 0
    total = 0
    for score in Score.objects.filter(user=player):
        total = total + 1
        percentage = percentage + score.get_shot_percentage()
    if percentage == 0: return 0
    return str(round(percentage / total, 2)) + "%"


def schedule(request):
    seasons = Season.objects.all().exclude(name='Casual')
    return render(request, 'game/schedule.html', {'seasons': seasons,
                                                  'number_of_weeks': range(1, 1 + seasons[0].number_of_weeks)})


def update_schedule(request):
    season_id = request.GET['season']
    week = request.GET['week']
    season = Season.objects.get(id=season_id)
    week_schedule = Game.objects.filter(season_id=season_id).filter(week=week)
    teams = format_schedule(week_schedule)
    return JsonResponse({'schedule': teams,
                         'weeks': list(range(1, 1 + season.number_of_weeks))})


def team_schedule(request, pk):
    # TODO: Might need a season filter here
    team_schedule = Game.objects.filter(away_team_id=pk) | Game.objects.filter(home_team_id=pk)
    schedule = team_schedule.order_by('week')
    form_schedule = format_schedule(schedule)
    return JsonResponse({'schedule': form_schedule})


def format_schedule(week_schedule):
    teams = []
    for game in week_schedule:
        teams.append({'home_team': list(Team.objects.filter(pk=game.home_team.pk).values()),
                      'away_team': list(Team.objects.filter(pk=game.away_team.pk).values()),
                      'game_id': game.pk})
    return teams


@login_required
def get_teams(request):
    if request.method == "GET":
        game_type = request.GET['game_type']
        if game_type == 'casual':
            return JsonResponse({'home_team_name': "Test 1",
                                 'away_team_name': "Test 2"})
        return JsonResponse({'home_team_name': "BIG",
                             'away_team_name': "PROBLEM"})


class TeamListView(ListView):
    queryset = Team.objects.exclude(name="Blue").exclude(name="Red")
    context_object_name = 'teams'
    template_name = 'game/list_teams.html'
    ordering = ['-wins']


def game_stats_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    home_scores = []
    away_scores = []
    for player in game.home_team.players.all():
        home_scores += list(Score.objects.filter(game=game, user=player).order_by('-top_makes'))
    for player in game.away_team.players.all():
        away_scores += list(Score.objects.filter(game=game, user=player).order_by('-top_makes'))

    return render(request, 'game/game_stats.html', {'home_scores': home_scores,
                                                    'away_scores': away_scores,
                                                    'game': game})


class TeamMemberListView(ListView):
    model = Team
    context_object_name = 'teams'
    template_name = 'game/view_team.html'
    ordering = 'first_name'


class PlayerListView(ListView):
    model = User
    context_object_name = 'players'
    template_name = 'game/list_players.html'
    ordering = 'first_name'
