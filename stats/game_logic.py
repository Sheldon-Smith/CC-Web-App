from importlib import import_module
from operator import add

import copy

from settings import base

from game.models import Team, Season, Game, TeamMember, Score
from account.models import User

SessionStore = import_module(base.SESSION_ENGINE).SessionStore


TOP = 0
TOP_GAY = 1
BOTTOM = 2
BOTTOM_GAY = 3
MISS = 4

PLAYERS_FOR_BALLS_BACK = 2

DBL_STUFFS_TO_WIN = 2

OVERTIME_CUPS = [6, 3, 1]

FIELDS = ['in_game',
          'home_team_name',
          'away_team_name',
          'home_team_cups',
          'away_team_cups',
          'home_team_players',
          'away_team_players',
          'shooter_index',
          'current_team_index',
          'shot_state',
          'game_state',
          'double_stuff',
          'overtime',
          'closer',
          'num_players',
          'shooters',
          'shots_made',
          'double_to_win',
          'home_to_drink',
          'away_to_drink',
          'stats_array']


def load_game(django_session):

    game_session = django_session.get('game', None)
    if not game_session:
        # Initialize an empty dict for the game state
        django_session['game'] = {}
    game_session = django_session['game']
    return game_session


def save_game(django_session, game_session):
    django_session['game'] = game_session


def restore_undo_state(django_session):
    return django_session['game'].get('undo_state', None)


def save_undo_state(django_session, game_session):
    django_session['game']['undo_state'] = copy.deepcopy(game_session)


def init_game(session, body):
    session['in_game'] = True
    session['game_id'] = body['game_id']
    session['home_team_name'] = body['home_team_name']
    session['away_team_name'] = body['away_team_name']
    session['home_team_cups'] = 100
    session['away_team_cups'] = 100
    session['home_team_players'] = body['home_team_players']
    session['away_team_players'] = body['away_team_players']
    session['shooter_index'] = 0
    session['current_team_index'] = 0
    session['shot_state'] = 'shooting'
    session['game_state'] = 'normal'
    session['double_stuff'] = 0
    session['overtime'] = 0
    session['closer'] = 0  # The index of the team that enters a shoot to win state
    session['num_players'] = len(body['home_team_players'])
    session['shooters'] = list(range(session['num_players']))
    session['shots_made'] = []
    session['double_to_win'] = 2
    session['home_to_drink'] = 0
    session['away_to_drink'] = 0
    stats_array = [[0, 0, 0, 0, 0, 100] for i in range(session['num_players'])]
    session['stats_array'] = [stats_array, stats_array]
    session['undo_state'] = []
    session['undo'] = 1


def update_stats(session, body):
    shooters = session['shooters']
    shooter_idx = session['shooter_index']
    current_team_idx = session['current_team_index']
    current_player_idx = shooters[shooter_idx]
    game_state = session['game_state']

    shot_data = body['shot_data']
    stats = session['stats_array'][current_team_idx][current_player_idx]
    stats = list(map(add, stats, shot_data))
    session['stats_array'][current_team_idx][current_player_idx] = stats
    shot_state = session['shot_state']
    closer = session['closer']

    if not shot_data[MISS]:
        session['shots_made'].append(current_player_idx)
        if current_team_idx:  # away is shooting
            session['home_to_drink'] = (session['home_to_drink'] + 1) % session['num_players']
        else:
            session['away_to_drink'] = (session['away_to_drink'] + 1) % session['num_players']
        if game_state == 'shoot_to_win':
            session['double_stuff'] += 1
        else:
            if current_team_idx:  # away is shooting
                session['home_team_cups'] -= 1
                if session['home_team_cups'] == 0:
                    game_state = 'shoot_to_win'
                    if shot_state != 'redemption':
                        closer = current_team_idx
            else:
                session['away_team_cups'] -= 1
                if session['away_team_cups'] == 0:
                    game_state = 'shoot_to_win'
                    if shot_state != 'redemption':
                        closer = current_team_idx

    session['game_state'] = game_state
    session['closer'] = closer


def update_shot_state(session, body):
    num_players = session['num_players']
    shooters = session['shooters']
    shooter_idx = session['shooter_index']
    current_team_idx = session['current_team_index']
    shots_made = session['shots_made']
    shot_state = session['shot_state']
    miss = body['shot_data'][MISS]
    game_state = session['game_state']

    if shot_state == 'shooting':
        if shooter_idx == (len(shooters) - 1):
            shooter_idx = 0
            if len(shots_made) >= PLAYERS_FOR_BALLS_BACK:
                shooters = shots_made
            else:
                shooters = list(range(num_players))
                current_team_idx = not current_team_idx
                if game_state == 'shoot_to_win':
                    game_state = 'check_win'
            shots_made = []
        else:
            shooter_idx += 1
    else:  # redemption
        if miss:
            shooter_idx += 1
        if shooter_idx == len(shooters):
            if game_state == 'shoot_to_win':
                game_state = 'check_win'
            else:
                game_state = 'game_over'
            shooter_idx = 0

    session['shot_state'] = shot_state
    session['current_team_index'] = current_team_idx
    session['shooter_index'] = shooter_idx
    session['shooters'] = shooters
    session['shots_made'] = shots_made
    session['game_state'] = game_state


def update_game_state(session, body):
    home_cups = session['home_team_cups']
    away_cups = session['away_team_cups']
    game_state = session['game_state']
    double_stuff = session['double_stuff']
    current_team_idx = session['current_team_index']
    closer = session['closer']
    shot_state = session['shot_state']
    overtime = session['overtime']
    double_to_win = session['double_to_win']
    shooters = session['shooters']
    shots_made = session['shots_made']
    num_players = session['num_players']

    if game_state == 'check_win' or double_stuff == double_to_win:
        if double_stuff == DBL_STUFFS_TO_WIN:
            if closer == current_team_idx:
                game_state = 'game_over'
                shot_state = 'shooting'
            else:
                game_state = 'overtime'
                shot_state = 'shooting'
        else:
            if closer == current_team_idx:
                game_state = 'overtime'
                shot_state = 'shooting'
                current_team_idx = not current_team_idx
            else:
                if shot_state == 'redemption':
                    game_state = 'overtime'
                    shot_state = 'shooting'
                    current_team_idx = not current_team_idx
                else:
                    shot_state = 'redemption'
                    double_stuff = 0
                    game_state = 'normal'

    if game_state == 'overtime':
        home_cups = OVERTIME_CUPS[overtime]
        away_cups = OVERTIME_CUPS[overtime]
        shot_state = 'shooting'
        game_state = 'normal'
        double_stuff = 0
        shooters = list(range(num_players))
        shots_made = []
        overtime = (overtime + 1 if overtime < len(OVERTIME_CUPS) else 2)
        double_to_win = 1

    session['game_state'] = game_state
    session['double_to_win'] = double_to_win
    session['overtime'] = overtime
    session['home_team_cups'] = home_cups
    session['away_team_cups'] = away_cups
    session['double_stuff'] = double_stuff
    session['shot_state'] = shot_state
    session['current_team_index'] = current_team_idx
    session['shooters'] = shooters
    session['shots_made'] = shots_made


def game_over(session):
    game_id = session['game_id']
    if game_id == 'None':
        season = Season.objects.get(name="Casual")
        home_team = Team.objects.get(name='Blue')
        away_team = Team.objects.get(name='Red')
        game = Game.objects.create(home_team=home_team,
                                   away_team=away_team,
                                   season=season)
    else:
        game = Game.objects.get(pk=int(game_id))
        home_team = game.home_team
        away_team = game.away_team
        season = game.season
    game.home_cups = session['home_cups']
    game.away_cups = session['away_cups']
    if session['home_cups'] > session['away_cups']:
        winner = home_team
        loser = away_team
    else:
        winner = away_team
        loser = home_team
    game.winner = winner
    game.loser = loser
    stats_array = session['stats_array']
    home_away = ['home_team_players', 'away_team_players']
    home_away_objs = [home_team, away_team]
    for i in range(len(home_away)):
        for j in range(session['num_players']):
            player_id = session.get(home_away[i])[j][1]
            player = User.objects.get(pk=player_id)
            team_member = home_away_objs[i].players.filter(pk=player_id)
            if not team_member:
                TeamMember.objects.create(team=home_away_objs[i], player=player, season=season)
            Score.objects.create(user=player,
                                 top_makes=stats_array[i][j][TOP],
                                 top_gays=stats_array[i][j][TOP_GAY],
                                 bottom_makes=stats_array[i][j][BOTTOM],
                                 bottom_gays=stats_array[i][j][BOTTOM_GAY],
                                 misses=stats_array[i][j][MISS],
                                 game=game)
