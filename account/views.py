from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from account.forms import SignUpForm

from django.contrib.auth import login as account_login

from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from account.models import User


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.grad_year = form.cleaned_data.get('grad_year')
            user.save()
            account_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def get_players(request):
    if request.method == 'GET':
        return JsonResponse({'players': list(User.objects.values_list('first_name', 'last_name', 'pk'))})


def user_account(request, name, pk):
    user = get_object_or_404(User, first_name=name, pk=pk)
    return render(request, 'registration/user_account.html', {'user_account': user})