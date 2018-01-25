import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from game.models import Game
from stats.game_logic import update_stats, init_game, update_shot_state, update_game_state, game_over, \
    load_game, save_game, restore_undo_state, save_undo_state

BASE_NUM_PLAYERS = 6

PERCENT_IDX = 5
MISS = 4


@login_required
def create_game_view(request):
    session = load_game(request.session)
    if not session.get('in_game', False):
        home_team_name = "Blue"
        away_team_name = "Red"
        game_id = None
        if request.GET.get('game', False):
            game_id = request.GET['game']
            game = Game.objects.get(pk=game_id)
            if game.home_team.can_keep_stats(request.user) or game.away_team.can_keep_stats(request.user):
                home_team_name = game.home_team.name
                away_team_name = game.away_team.name
            else:
                return redirect('game_stats_view', game_id)
        value_dict = dict()
        # Start counting from 1
        value_dict['home_team_name'] = home_team_name
        value_dict['away_team_name'] = away_team_name
        value_dict['num_iter'] = range(1, BASE_NUM_PLAYERS + 1)
        value_dict['num_players'] = BASE_NUM_PLAYERS
        value_dict['game_id'] = game_id
        return render(request, 'stats/create_game.html', value_dict)
    return redirect('game_view')


@login_required
def game_view(request):
    session = load_game(request.session)
    if session.get('in_game', False):
        value_dict = dict()
        value_dict['home_team_name'] = session.get("home_team_name")
        value_dict['away_team_name'] = session.get("away_team_name")
        value_dict['home_team_players'] = session['home_team_players']
        value_dict['away_team_players'] = session['away_team_players']
        save_game(request.session, session)
        return render(request, 'stats/game.html', value_dict)
    return redirect('create_game_view')


@login_required
@csrf_exempt
def init_game_logic(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        session = load_game(request.session)
        init_game(session, body)
        save_game(request.session, session)
        return JsonResponse({'redirect': '/stats/game'})
    return JsonResponse({'redirect': '/stats/create_game'})


@login_required
@csrf_exempt
def quit_game_logic(request):
    session = load_game(request.session)
    if not session.get('in_game', False):
        return redirect(create_game_view)
    session['in_game'] = False
    save = request.POST['save']
    if int(save):
        game_over(session)
    save_game(request.session, session)
    return JsonResponse({'redirect': '/'})


@login_required
@csrf_exempt
def pull_logic(request):
    session = load_game(request.session)
    if not session.get('in_game', False):
        return redirect(create_game_view)
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        if body['team']:  # away team pull cups
            session['away_team_cups'] -= 1
        else:
            session['home_team_cups'] -= 1
        save_game(request.session, session)
        return HttpResponse("OK")
    return HttpResponse("Must be post")


@login_required
@csrf_exempt
def shot_logic(request):
    session = load_game(request.session)
    if not session.get('in_game', False):
        return redirect(create_game_view)
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        session['undo'] = 0
        save_undo_state(request.session, session)
        update_stats(session, body)
        update_shot_state(session, body)
        update_game_state(session, body)
        save_game(request.session, session)
        return HttpResponse("OK")
    return HttpResponse("Must be POST")


@login_required
def game_state(request):
    session = load_game(request.session)
    if not session.get('in_game', False):
        return redirect(create_game_view)
    if request.method == "GET":
        stats = session['stats_array']
        current_player = session['shooter_index']
        current_player = session['shooters'][current_player]
        current_team_idx = session['current_team_index']
        if current_team_idx:  # Away team is shooting
            current_player = session['away_team_players'][current_player][0]
        else:
            current_player = session['home_team_players'][current_player][0]
        home_cups = session['home_team_cups']
        away_cups = session['away_team_cups']
        cups_hit = len(session['shots_made'])
        if current_team_idx:  # away
            to_drink = session['home_team_players'][session['home_to_drink']][0]
        else:
            to_drink = session['away_team_players'][session['away_to_drink']][0]
        percent = int(abs(home_cups-away_cups)/2)
        if home_cups > away_cups:
            away_percent = 50 - percent
            home_percent = 50 + percent
        else:
            away_percent = 50 + percent
            home_percent = 50 - percent
        player_total_makes = 0
        player_total_shots = 0
        for team in range(len(stats)):
            for player in range(len(stats[team])):
                for player_stats in range(len(stats[team][player]) - 1):  # Minus 1 because we dont want percent stats
                    stat = stats[team][player][player_stats]
                    if player_stats == MISS:
                        player_total_shots = player_total_makes + stat
                    else:
                        player_total_makes += stat
                try:
                    stats[team][player][PERCENT_IDX] = int(player_total_makes/player_total_shots*100)
                except ZeroDivisionError:
                    stats[team][player][PERCENT_IDX] = 100
                player_total_shots = 0
                player_total_makes = 0

        if session['game_state'] == 'game_over':
            game_over(session)
            save_game(request.session, session)
            return redirect('home')
        save_game(request.session, session)
        return JsonResponse({'current_player': current_player,
                             'stats_array': stats,
                             'home_cups': home_cups,
                             'away_cups': away_cups,
                             'home_percent': home_percent,
                             'away_percent': away_percent,
                             'current_team': current_team_idx,
                             'cups_hit': cups_hit,
                             'to_drink': to_drink})


@login_required
@csrf_exempt
def undo_logic(request):
    session = load_game(request.session)
    if not session['undo']:
        session['undo'] = 1
        session = restore_undo_state(request.session)
        if session:
            save_game(request.session, session)
        return HttpResponse("OK")
    else:
        return HttpResponse("Cannot undo again")
