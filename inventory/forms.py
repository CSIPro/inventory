from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# All this shit is something that could be moved to seperate app (for modularity).


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['pic']

        labels = {
            'pic': 'Profile Pic',
        }
