from account.forms import SignUpForm

from django.contrib.auth import login as account_login

from django.shortcuts import redirect
from django.shortcuts import render


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
