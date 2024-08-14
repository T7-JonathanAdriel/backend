from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ..models import CustomUser

class CustomUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = CustomUser
    fields = ['username', 'name', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
  class Meta:
    model = CustomUser
    fields = ['username', 'password']
    