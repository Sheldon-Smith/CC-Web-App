from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from account.forms import SignUpForm

from django.contrib.auth import login as account_login

from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from account.models import User
from game.models import Score, Game

EMAIL_SUBJECT = '[CCLeague] Account Creation'
EMAIL_CONTENT = 'Thank you for creating a CCLeague account. ' \
                'The commissioner has been notified and will activate your account shortly.'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.grad_year = form.cleaned_data.get('grad_year')
            user.save()
            user.email_user(EMAIL_SUBJECT, EMAIL_CONTENT)
            account_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# TODO this view doesnt belong here
@login_required
def get_players(request):
    if request.method == 'GET':
        if request.GET['game_id'] != 'None':
            game = Game.objects.get(pk=request.GET['game_id'])
            return JsonResponse({'home_players': list(game.home_team.players.order_by('first_name')
                                                      .values_list('first_name', 'last_name', 'pk')),
                                 'away_players': list(game.away_team.players.order_by('first_name')
                                                      .values_list('first_name', 'last_name', 'pk'))
                                })
        players = list(User.objects.order_by('first_name').values_list('first_name', 'last_name', 'pk'))
        return JsonResponse({'home_players': players,
                             'away_players': players})


def user_account(request, name, pk):
    user = get_object_or_404(User, first_name=name, pk=pk)
    scores = Score.objects.filter(user=user)
    return render(request, 'registration/user_account.html',
                  {'user_account': user,
                   'scores': scores})
