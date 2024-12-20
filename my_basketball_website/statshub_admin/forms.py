from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms




class SignupUserForm(UserCreationForm):

    class Meta:
        model = User # Inheriting from the django Users

        #You can either use a list or tuple to collect the fields inputs
        fields = ('username', 'email', 'password1', 'password2' )# Fields to fill in the form