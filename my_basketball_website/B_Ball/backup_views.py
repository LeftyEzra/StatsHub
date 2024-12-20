"""from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import  ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views import View

from django.urls import reverse_lazy


from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from .models import PlayersStats, Player, Team, BackgroundImages, GameSchedule,QuarterlyScores, Organizer,  Competition, Standing
from django.db.models import Q
from .forms import OrganizerForm, CompetitionForm, TeamForm, PlayerFormSet
from django.core.paginator import Paginator




from django.db.models import Sum, F, Value, IntegerField,ExpressionWrapper, FloatField
from django.db.models.functions import Cast # Casting string to integer
import pandas as pd

from datetime import datetime, timedelta # Module to represent the fifference between two dates
from django.utils.timezone import now
from django .utils import timezone
from calendar import HTMLCalendar
from datetime import date
from operator import itemgetter"""





# Delete Team(s)
"""def delete_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    team.delete()
    # Return an 'invalid login' error message.
    messages.success(request, (" Team deleted successfully):"))
    return redirect('list-all-teams')"""


# Update Team Views
"""def update_team(request, pk):

    # team_details = Team.object.get(id=pk)
    update_teams = get_object_or_404(Team, pk=pk)
    form = TeamForm(request.POST or None, instance=update_teams )

    if form.is_valid():
        form.save()
        # Return a valid update message.
        messages.success(request, (" Team Updated Sucessfully ):"))
        return redirect('list-all-teams')
    return render(request, 'update_team.html', {'update_teams': update_teams,
                                                'form':form, })"""




#Forms to database view
"""def forms_db(request):
    submitted = False
    if request.method == "POST":
        form = TeamForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            # Return an 'invalid login' error message.
            messages.success(request, (" Team Added Successfully ):"))
            return HttpResponseRedirect('/forms_db?submitted=True')
    else:
        form = TeamForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'forms.html', {"form" : form, 'submitted':submitted})"""





#Team Roster
"""def team_roster(request,pk):
    teams_details = get_object_or_404(Team, pk=pk)
    players = teams_details.players.all()  # Using the foreign key Team related_name  'players'
    return render(request, 'team_roster.html', {'team_details': teams_details, 'players': players})"""



"""
def teams_id(request, pk):
    team_details = get_object_or_404(Team, pk=pk)
    team_images = BackgroundImages.objects.filter(team_pictures=team_details)
    players = team_details.players.all()  # Using the foreign key Team related_name 'players'
    games = GameSchedule.objects.all()


    context = {
        'team_details': team_details,
        'team_images': team_images,
        'games': games,
        'players': players,
        'timestamp': now().timestamp(),  # Generate a unique timestamp to ensure that the browser loads the latest version of the .js file
    }
    return render(request, 'team_details.html', context)"""


"""def list_all_teams(request):
    teams = Team.objects.all()
    for team in teams:
        print(f"Team: {team.team_name}, Logo: {team.team_logo}")
        if not team.team_logo:
            team.team_logo = 'uploads/Team_Logos/default_logo.png'
    return render(request, 'list_all_teams.html', {'teams': teams})"""





"""
class OrganizerCreate(View):
    def get(self, request):
        form = OrganizerForm()
        submitted = 'submitted' in request.GET
        return render(request, 'organizer_registration.html', {"form": form, 'submitted': submitted})

    def post(self, request):
        form = OrganizerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Organizer Added Successfully :)")
            return redirect('/create_organizer?submitted=True')
        return render(request, 'organizer_registration.html', {"form": form, 'submitted': False})"""


"""class CompetitionList(View):
    def get(self, request):
        competitions = Competition.objects.all().order_by('name')
        organizers = Organizer.objects.all().order_by('name')

        for competition in competitions:
            if not competition.competition_logo:
                competition.competition_logo = 'uploads/Competition_Logos/default_logo.png'

        return render(request, 'list_all_organizers.html', {
            'competitions': competitions,
            'organizers': organizers
        })"""



"""class CompetitionUpdateView(UpdateView):
    model = Competition
    form_class = CompetitionForm
    template_name = 'competition_update_form.html'
    success_url = '/list-all-organizers/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            competition_update_form = self.get_form()
            if competition_update_form.is_valid():
                messages.success(request, "Competition Updated Successfully :)")
                return self.form_valid(competition_update_form)

            else:
                return self.form_invalid(competition_update_form)
        return super().post(request, *args, **kwargs)"""