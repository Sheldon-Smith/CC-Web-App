from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from account.choices import CLASS_CHOICES


class SignUpForm(UserCreationForm):
    grad_year = forms.ChoiceField(choices=CLASS_CHOICES, required=True)
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'grad_year',
                  'password1',
                  'password2')
