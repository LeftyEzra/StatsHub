from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
#from .models import Basketball_Stats

from calendar import HTMLCalendar
from django .utils import timezone
from datetime import datetime
import datetime as dt

# Create your views here.

# Home view
def home(request):

    time = datetime.now().strftime("%H:%M")
    #players = Basketball_Stats.objects.all().order_by('jersey_numbers')

    return render(request, 'home.html', {})

# About view
def about(request):
    return render(request, 'about.html', {})

def stats_tables(request):
    pass
    #players = Basketball_Stats.objects.all().order_by('jersey_numbers')
    #return render(request, 'tables.html', {'players': players})
