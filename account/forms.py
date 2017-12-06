
from django.contrib.auth.forms import UserCreationForm

from account.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',
                  'first_name',
                  'last_name',
                  'grad_year',
                  'password1',
                  'password2')
