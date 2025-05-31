from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Track
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class AddTrackForm(forms.Form):
    track = forms.ModelChoiceField(queryset=Track.objects.all(), label="Select Track")