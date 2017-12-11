import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from stats.game_logic import update_stats, init_game, update_shot_state, update_game_state, restore_state, game_over

BASE_NUM_PLAYERS = 6

PERCENT_IDX = 5
MISS = 4


@login_required
def create_game_view(request):
    if not request.session.get('in_game', False):
        value_dict = dict()
        # Start counting from 1
        value_dict['num_iter'] = range(1, BASE_NUM_PLAYERS + 1)
        value_dict['num_players'] = BASE_NUM_PLAYERS
        return render(request, 'stats/create_game.html', value_dict)
    return redirect('game_view')


@login_required
def game_view(request):
    session = request.session
    if session.get('in_game', False):
        value_dict = dict()
        value_dict['home_team_name'] = session.get("home_team_name")
        value_dict['away_team_name'] = session.get("away_team_name")
        value_dict['home_team_players'] = session['home_team_players']
        value_dict['away_team_players'] = session['away_team_players']
        return render(request, 'stats/game.html', value_dict)
    return redirect('create_game_view')


@login_required
@csrf_exempt
def init_game_logic(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        init_game(request.session, body)
        return JsonResponse({'redirect': '/stats/game'})
    return JsonResponse({'redirect': '/stats/create_game'})


@login_required
@csrf_exempt
def quit_game_logic(request):
    if not request.session.get('in_game', False):
        return redirect(create_game_view)
    request.session['in_game'] = False
    save = request.POST['save']
    if save:
        game_over(request.session)
    return JsonResponse({'redirect': '/'})


@login_required
@csrf_exempt
def pull_logic(request):
    if not request.session.get('in_game', False):
        return redirect(create_game_view)
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        if body['team']:  # away team pull cups
            request.session['away_team_cups'] -= 1
        else:
            request.session['home_team_cups'] -= 1
        return HttpResponse("OK")
    return HttpResponse("Must be post")


@login_required
@csrf_exempt
def shot_logic(request):
    if not request.session.get('in_game', False):
        return redirect(create_game_view)
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        update_stats(request.session, body)
        update_shot_state(request.session, body)
        update_game_state(request.session, body)
        print(request.session['game_state'])
        print(request.session['shot_state'])
        print(request.session['current_team_index'])
        return HttpResponse("OK")
    return HttpResponse("Must be POST")


@login_required
def game_state(request):
    if not request.session.get('in_game', False):
        return redirect(create_game_view)
    if request.method == "GET":
        stats = request.session['stats_array']
        current_player = request.session['shooter_index']
        current_player = request.session['shooters'][current_player]
        current_team_idx = request.session['current_team_index']
        if current_team_idx:  # Away team is shooting
            current_player = request.session['away_team_players'][current_player][0]
        else:
            current_player = request.session['home_team_players'][current_player][0]
        home_cups = request.session['home_team_cups']
        away_cups = request.session['away_team_cups']
        cups_hit = len(request.session['shots_made'])
        if current_team_idx:  # away
            to_drink = request.session['home_team_players'][request.session['home_to_drink']][0]
        else:
            to_drink = request.session['away_team_players'][request.session['away_to_drink']][0]
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

        if request.session['game_state'] == 'game_over':
            game_over(request.session)
            return redirect('home')
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
    if not request.session['undo']:
        print("undo")
        request.session['undo'] = 1
        restore_state(request.session)
        return HttpResponse("OK")
    else:
        print("no undo")
        return HttpResponse("Cannot undo again")
