from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
#from .forms import ResgisterUserForm
from .forms import SignupUserForm

# Create your views here.

def login_user(request):
    # Django authentication code
    if request.method == 'POST': # If the users goes to the login page and fill out the form
        username = request.POST["username"] # Username
        password = request.POST["password"] # Password
        user = authenticate(request, username=username, password=password) # Check if the username and password variable are correct
        if user is not None: # if the user fill the form and the variables are correct
            login(request, user)# log the user in
            return redirect("home")   # Redirect to home page after a successful log in.

        else:
            # Else if the password or username is incorrect, return an 'invalid login' error message.
            messages.success(request, ("Oops! Error Logging In, Try Again... "))
            return redirect('login-user') # Remain in login page.

    else:
        return render(request, 'authentication/login.html', {})


# Logout View
def logout_user(request):
    logout(request)
    messages.success(request, ("Thanks for spending some quality time with the web site today. You are logged out..."))
    return redirect('home')


# Create User Form
"""def register_user(request):
    if request.method == 'POST':
        form = ResgisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful! ):") )
            return redirect("home")
    else:
        form = ResgisterUserForm()

    return render(request, 'authentication/register_user.html', {"form":form})"""



# Create User Form
def register_user(request):
    if request.method == 'POST':
        form = SignupUserForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('login-user')

    else:
        form = SignupUserForm()

    return render(request, 'authentication/register_user.html', {"form":form})
