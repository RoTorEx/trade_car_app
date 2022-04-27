from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import UserProfile


class UserProfileCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = UserProfile
        fields = ('username', 'email', 'role')


class UserProfileChangeForm(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'role')
        # exclude = ['first_name', 'last_name', 'date_joined']  # ignore fields
