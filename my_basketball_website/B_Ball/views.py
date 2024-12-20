from django.shortcuts import render, get_object_or_404
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
from .forms import OrganizerForm, CompetitionForm, TeamForm, PlayerFormSet, PlayerForm
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory




from django.db.models import Sum, F, Value, IntegerField,ExpressionWrapper, FloatField
from django.db.models.functions import Cast # Casting string to integer
import pandas as pd

from datetime import datetime, timedelta # Module to represent the fifference between two dates
from django.utils.timezone import now
from django .utils import timezone
from calendar import HTMLCalendar
from datetime import date
from operator import itemgetter




"""


GameSchedule.objects.filter(...)
GameSchedule: model that holds the game schedules.
objects: Manager for interacting with the database.
filter(...): This is used to get records that match certain conditions.
competition_game_schedule=competition
competition_game_schedule: This is the ForeignKey field in your GameSchedule model that links to the Competition model.
competition: This is the current competition instance being processed in the loop.
date=current_date

current_date: This is the specific date being processed in the loop.
.distinct()
distinct(): This ensures that the query returns distinct records, so you don't get duplicate entries.
Date: For each date within the competition's date range, you fetch game schedules.
Filter: You filter the game schedules by the competition and date.
Distinct: Ensures no duplicates in the results.

"""








# Create your views here.


#find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
#find . -path "*/migrations/*.pyc"  -delete








class GetGamesByDate(View):
    def get(self, request, competition_id, date):
        competition = get_object_or_404(Competition, pk=competition_id)
        games = GameSchedule.objects.filter(competition_game_schedule=competition, date=date).distinct()
        return render(request, 'organizer_details.html', {'games': games})

class GetTopAverages(View):
    def get(self, request, competition_id):
        competition = get_object_or_404(Competition, pk=competition_id)
        all_teams = competition.teams.all()
        players = Player.objects.filter(team_name__in=all_teams).order_by('jersey_numbers')

        # Fetch standings for the specific competition using __in lookup
        standings = Standing.objects.filter(team__in=all_teams, competition=competition).order_by('-games_won')

        # Prepare dictionaries to hold total points scored and conceded
        team_points_scored = {}
        team_points_conceded = {}

        # Calculate total points scored and conceded for each team
        for team in all_teams:
            home_scores = GameSchedule.objects.filter(home_team=team, competition_game_schedule=competition).aggregate(Sum('home_team_scores'))['home_team_scores__sum'] or 0
            away_scores = GameSchedule.objects.filter(away_team=team, competition_game_schedule=competition).aggregate(Sum('away_team_scores'))['away_team_scores__sum'] or 0
            total_points_scored = home_scores + away_scores

            home_conceded = GameSchedule.objects.filter(home_team=team, competition_game_schedule=competition).aggregate(Sum('away_team_scores'))['away_team_scores__sum'] or 0
            away_conceded = GameSchedule.objects.filter(away_team=team, competition_game_schedule=competition).aggregate(Sum('home_team_scores'))['home_team_scores__sum'] or 0
            total_points_conceded = home_conceded + away_conceded

            team_points_scored[team.id] = total_points_scored
            team_points_conceded[team.id] = total_points_conceded

        # Prepare standings data
        standings_data = []
        for standing in standings:
            team_id = standing.team.id
            total_points_scored = team_points_scored.get(team_id, 0)  # Default to 0 if no points found
            total_points_conceded = team_points_conceded.get(team_id, 0)  # Default to 0 if no points found

            standing_data = {
                'team': standing.team.team_name,
                'games_played': standing.games_won + standing.games_lost,
                'games_won': standing.games_won,
                'games_lost': standing.games_lost,
                'game_win_loss_percent': ((standing.games_won / (standing.games_won + standing.games_lost)) * 100),
                'points_scored': total_points_scored,
                'points_conceded': total_points_conceded,
                'point_diff': total_points_scored - total_points_conceded,
                'points_scored_per_game': total_points_scored / (standing.games_won + standing.games_lost),
                'points_conceded_per_game': total_points_conceded / (standing.games_won + standing.games_lost),
                'point_difference_per_game': (total_points_scored / (standing.games_won + standing.games_lost)) - (total_points_conceded / (standing.games_won + standing.games_lost)),
                #'expected_winning_percentage': standing.expected_winning_percentage,
            }
            standings_data.append(standing_data)

        # Fetch player stats for players in the competition
        player_stats = PlayersStats.objects.filter(player_name__in=players).order_by('points')



        players_data = list(players)

        context = {
            'competition': competition,
            'all_teams': all_teams,
            'players': players_data,  # Converting QuerySet to list for better readability
            'player_stats': player_stats,
            'standings': standings_data,
        }
        return render(request, 'game_schedule.html', context)











#Game summary view
def game_summary(request, pk):
    game = get_object_or_404(GameSchedule, pk=pk)
    quarterly_scores = get_object_or_404(QuarterlyScores, game=game)

    context = {
        'game': game,
        'quarterly_scores': quarterly_scores,
    }
    return render(request, 'game_summary.html', context)




# Search team view
def search_teams_players(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        searched = Team.objects.filter(Q(team_name__icontains=searched) | Q(team_abbreviation__icontains=searched)) # Query the Database for the teams
        if not searched:
            # Return an 'invalid search' error message.
            messages.success(request, (" Team not in list. Please search another team ):"))
            return render(request, 'search_teams_players.html',
                          {})
        else:
            return render(request, 'search_teams_players.html',
                      {'searched': searched})
    else:
        return render(request, 'search_teams_players.html',
                      {})





def stats_tables(request, game_pk):
    game = get_object_or_404(GameSchedule, pk=game_pk) # Game played
    home_team = game.home_team # Home team
    away_team = game.away_team # Away Team

    home_team_players = PlayersStats.objects.filter(player_team=home_team).order_by('-points') # Home team players stats
    away_team_players = PlayersStats.objects.filter(player_team=away_team).order_by('-points') # Away team players stats

    # Using django aggregate function to calculate the sum of all the players stats metrics
    home_totals = home_team_players.aggregate(

        points=Sum('points'),
        field_goal_attempts=Sum('field_goal_attempts'),
        field_goal_made=Sum('field_goal_made'),

        point_3_attempts=Sum('point_3_attempts'),
        point_3_made = Sum('point_3_made'),

        point_2_attempts = Sum('point_2_attempts'),
        point_2_made = Sum('point_2_made'),

        ft_attempts=Sum('ft_attempts'),
        ft_made = Sum('ft_made'),

        offensive_rebs = Sum('offensive_rebs'),
        defensive_rebs = Sum('defensive_rebs'),
        total_rebounds = Sum('total_rebounds'),
        blocks = Sum('blocks'),
        assists = Sum('assists'),
        steals = Sum('steals'),
        turnovers = Sum('turnovers'),
        personal_fouls = Sum('personal_fouls'),
        plus_minus=Sum(Cast(F('plus_minus'), IntegerField())),
        efficiency=Sum(Cast(F('efficiency'), IntegerField()))

    )
    # Calculating the percentages manually
    # The if conditional statement is to print 0 if no attempts is recorded
    home_totals['fg_percent'] = (home_totals['field_goal_made'] / home_totals['field_goal_attempts'] * 100) if home_totals['field_goal_attempts'] else 0
    home_totals['point_3_percent'] = (home_totals['point_3_made'] / home_totals['point_3_attempts'] * 100) if home_totals['point_3_attempts'] else 0
    home_totals['point_2_percent'] = (home_totals['point_2_made'] / home_totals['point_2_attempts'] * 100) if home_totals['point_2_attempts'] else 0
    home_totals['ft_percent'] = (home_totals['ft_made'] / home_totals['ft_attempts'] * 100) if home_totals['ft_attempts'] else 0


    # Using django aggregate function to calculate the sum of all the players stats metrics
    away_totals = away_team_players.aggregate(

        points=Sum('points'),
        field_goal_attempts=Sum('field_goal_attempts'),
        field_goal_made=Sum('field_goal_made'),

        point_3_attempts=Sum('point_3_attempts'),
        point_3_made=Sum('point_3_made'),

        point_2_attempts=Sum('point_2_attempts'),
        point_2_made=Sum('point_2_made'),

        ft_attempts=Sum('ft_attempts'),
        ft_made=Sum('ft_made'),

        offensive_rebs=Sum('offensive_rebs'),
        defensive_rebs=Sum('defensive_rebs'),
        total_rebounds=Sum('total_rebounds'),
        blocks=Sum('blocks'),
        assists=Sum('assists'),
        steals=Sum('steals'),
        turnovers=Sum('turnovers'),
        personal_fouls=Sum('personal_fouls'),
        plus_minus=Sum(Cast(F('plus_minus'), IntegerField())),
        efficiency=Sum(Cast(F('efficiency'), IntegerField()))
    )

    # Calculating the percentages manually
    # The if conditional statement is to print 0 if no attempts is recorded
    away_totals['fg_percent'] = (away_totals['field_goal_made'] / away_totals['field_goal_attempts'] * 100) if away_totals['field_goal_attempts'] else 0
    away_totals['point_3_percent'] = (home_totals['point_3_made'] / away_totals['point_3_attempts'] * 100) if away_totals['point_3_attempts'] else 0
    away_totals['point_2_percent'] = (away_totals['point_2_made'] / away_totals['point_2_attempts'] * 100) if away_totals['point_2_attempts'] else 0
    away_totals['ft_percent'] = (away_totals['ft_made'] / away_totals['ft_attempts'] * 100) if away_totals['ft_attempts'] else 0

    return render(request, 'tables.html', {
        'home_team_players': home_team_players,
        'away_team_players': away_team_players,
        'home_team': home_team,
        'away_team': away_team,
        'home_totals': home_totals,
        'away_totals': away_totals,
    })





# Home view
def home(request):

    time = datetime.now().strftime("%H:%M")
    players = Player.objects.all().order_by('jersey_numbers')

    return render(request, 'home.html', {'players':players})



# About view


"""def about_registration(request):
    team_form = TeamForm()
    formset = PlayerFormSet(queryset=Player.objects.none())  # Empty queryset for new team

    # Handle GET request for pagination
    p = Paginator(PlayerFormSet(queryset=Player.objects.none()), 1)  # Paginate formset with 1 form per page
    page = request.GET.get('page', 1)  # Default to page 1 if no page parameter is provided
    players_forms = p.get_page(page)

    if request.method == 'POST':
        team_form = TeamForm(request.POST, request.FILES)
        if team_form.is_valid():
            team = team_form.save()
            formset = PlayerFormSet(request.POST, request.FILES, instance=team)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Team and Players Added Successfully :)")
                return redirect('list-all-teams')
        else:
            formset = PlayerFormSet(request.POST, request.FILES)

    context = {
        'team_form': team_form,
        'players_forms': players_forms,
        'page': int(page)
    }
    return render(request, 'about_registration_form.html', context)"""


##################


def about_registration(request):
    team_form = TeamForm()
    formset = PlayerFormSet(queryset=Player.objects.none())  # Empty queryset for new team

    if request.method == 'POST':
        team_form = TeamForm(request.POST, request.FILES)
        formset = PlayerFormSet(request.POST, request.FILES)  # Initialize formset with POST data

        if team_form.is_valid():
            team = team_form.save()
            formset = PlayerFormSet(request.POST, request.FILES, instance=team)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Team and Players Added Successfully :)")
                return redirect('list-all-teams')
        else:
            formset = PlayerFormSet(request.POST, request.FILES)  # Reinitialize formset with POST data

    context = {
        'team_form': team_form,

        'formset': formset  # Pass the formset to the context
    }
    return render(request, 'about_registration_form.html', context)



#################











def about(request):
    team_form = TeamForm()
    formset = PlayerFormSet(queryset=Player.objects.none())  # Empty queryset for new team

    # Handle GET request for pagination
    p = Paginator(PlayerFormSet(queryset=Player.objects.none()), 1)  # Paginate formset with 1 form per page
    page = request.GET.get('page', 1)  # Default to page 1 if no page parameter is provided
    players_forms = p.get_page(page)

    if request.method == 'POST':
        team_form = TeamForm(request.POST, request.FILES)
        if team_form.is_valid():
            team = team_form.save()
            formset = PlayerFormSet(request.POST, request.FILES, instance=team)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Team and Players Added Successfully :)")
                return redirect('list-all-teams')
        else:
            formset = PlayerFormSet(request.POST, request.FILES)

    context = {
        'team_form': team_form,
        'players_forms': players_forms,
        'page': int(page)
    }
    return render(request, 'about.html', context)


def game_schedule(request):
    return render(request, 'game_schedule.html', {})

########################################################################################################
###################################     ORGANIZER      #################################################
########################################################################################################

# ORGANIZER CREATION
class OrganizerCreate(CreateView):
    model = Organizer
    form_class = OrganizerForm
    template_name = 'organizer_registration.html'
    success_url = '/list_all_organizers/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            organizer_form = self.get_form()
            if organizer_form.is_valid():
                messages.success(request, "Organizer Added Successfully :)")
                return self.form_valid(organizer_form)

            else:
                return self.form_invalid(organizer_form)
        return super().post(request, *args, **kwargs)




class OrganizerAndCompetitionList(View):
    def get(self, request):
        competitions = Competition.objects.all().order_by('name')
        organizers = Organizer.objects.all().order_by('name')

        for organizer in organizers:
            if not organizer.organizer_logo:
                organizer.organizer_logo = 'uploads/Organizer_Logos/default_logo.png'

        return render(request, 'list_all_organizers.html', {
            'competitions': competitions,
            'organizers': organizers
        })




# INDIVIDUAL ORGANIZER DETAILS
def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


class OrganizerDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        organizer = get_object_or_404(Organizer, pk=pk)
        competitions = Competition.objects.filter(organizers=organizer)

        competitions_with_dates = []
        for competition in competitions:
            date_range = []
            current_date = competition.start_date
            while current_date <= competition.end_date:
                games = GameSchedule.objects.filter(competition_game_schedule=competition, date=current_date).distinct()
                date_range.append({'date': current_date, 'games': list(games)})
                current_date += timedelta(days=1)
            competitions_with_dates.append({
                'competition': competition,
                'dates': date_range,
            })

        teams = Team.objects.filter(competition__in=competitions).distinct()
        standings = Standing.objects.filter(team__in=teams, competition__in=competitions)

        # Prepare dictionaries to hold total points scored and conceded
        team_points_scored = {}
        team_points_conceded = {}

        # Prepare a dictionary to hold accumulated standings
        accumulated_standings = {}

        # Calculate total points scored and conceded for each team
        for team in teams:
            home_scores = GameSchedule.objects.filter(
                home_team=team, competition_game_schedule__in=competitions
            ).aggregate(Sum('home_team_scores'))['home_team_scores__sum'] or 0

            away_scores = GameSchedule.objects.filter(
                away_team=team, competition_game_schedule__in=competitions
            ).aggregate(Sum('away_team_scores'))['away_team_scores__sum'] or 0

            total_points_scored = home_scores + away_scores

            home_conceded = GameSchedule.objects.filter(
                home_team=team, competition_game_schedule__in=competitions
            ).aggregate(Sum('away_team_scores'))['away_team_scores__sum'] or 0

            away_conceded = GameSchedule.objects.filter(
                away_team=team, competition_game_schedule__in=competitions
            ).aggregate(Sum('home_team_scores'))['home_team_scores__sum'] or 0

            total_points_conceded = home_conceded + away_conceded

            # Store total points scored and conceded
            team_points_scored[team.id] = total_points_scored
            team_points_conceded[team.id] = total_points_conceded

        # Accumulate standings data
        for standing in standings:
            team_id = standing.team.id
            # This is to display the initial stat of a team if their stats are not been updated
            if team_id not in accumulated_standings:
                accumulated_standings[team_id] = {
                    'team': standing.team.team_name,
                    'games_played': standing.games_won + standing.games_lost,
                    'games_won': standing.games_won,
                    'games_lost': standing.games_lost,
                    'points_scored': team_points_scored.get(team_id, 0),
                    'points_conceded': team_points_conceded.get(team_id, 0)
                }
            else:
                # Add the updated data if it's updated
                accumulated_standings[team_id]['games_played'] += standing.games_won + standing.games_lost
                accumulated_standings[team_id]['games_won'] += standing.games_won
                accumulated_standings[team_id]['games_lost'] += standing.games_lost
                accumulated_standings[team_id]['points_scored'] += team_points_scored.get(team_id, 0)
                accumulated_standings[team_id]['points_conceded'] += team_points_conceded.get(team_id, 0)


        # Preparing standings data
        standings_data = []
        for data in accumulated_standings.values():
            games_played = data['games_played']
            points_scored_per_game = data['points_scored'] / games_played if games_played > 0 else 0
            points_conceded_per_game = data['points_conceded'] / games_played if games_played > 0 else 0

            standing_data = {
                'team': data['team'],
                'games_played': games_played,
                'games_won': data['games_won'],
                'games_lost': data['games_lost'],
                'game_win_loss_percent': ((data['games_won'] / games_played) * 100) if games_played > 0 else 0,
                'points_scored': data['points_scored'],
                'points_conceded': data['points_conceded'],
                'point_diff': data['points_scored'] - data['points_conceded'],
                'points_scored_per_game': points_scored_per_game,
                'points_conceded_per_game': points_conceded_per_game,
                'point_difference_per_game': points_scored_per_game - points_conceded_per_game,
            }

            standings_data.append(standing_data)
            # Using lambda function to sort the games won in reverse order
            standings_data.sort(key=lambda x: x['games_won'], reverse=True)

        # Include players data for their various team
        players = Player.objects.filter(team_name__in=teams).order_by('player_name')
        player_stats = PlayersStats.objects.filter(player_name__in=players) # Filter players stats of each player

        #################################################################
        ################################################################

        # Ensure player name is included correctly in the DataFrame
        top_leaders_df = pd.DataFrame(player_stats.values('player_name__player_name', 'points', 'total_rebounds', 'assists', 'blocks','efficiency'))
        # Convert columns to numeric, coercing errors
        top_leaders_df[['points', 'total_rebounds', 'assists', 'blocks', 'efficiency']] = top_leaders_df[
            ['points', 'total_rebounds', 'assists', 'blocks', 'efficiency']].apply(pd.to_numeric, errors='coerce')

        # Calculate mean values for all players
        mean_df = top_leaders_df.groupby(["player_name__player_name"])[
            ['points', 'total_rebounds', 'assists', 'blocks', 'efficiency']].mean().reset_index()

        # Get top 5 players based on points, rebounds, and assists.
        top_5_points = mean_df[['player_name__player_name', 'points']].sort_values(by='points', ascending=False).head()
        top_5_rebounds = mean_df[['player_name__player_name', 'total_rebounds']].sort_values(by='total_rebounds',
                                                                                             ascending=False).head()
        top_5_assists = mean_df[['player_name__player_name', 'assists']].sort_values(by='assists',
                                                                                     ascending=False).head()
        top_5_blocks = mean_df[['player_name__player_name', 'blocks']].sort_values(by='blocks', ascending=False).head()
        top_5_efficiencies = mean_df[['player_name__player_name', 'efficiency']].sort_values(by='efficiency',
                                                                                             ascending=False).head()

        # Calculate top single game stats
        points_leaders_dfs = top_leaders_df[['player_name__player_name', 'points']].sort_values(by='points',
                                                                                                ascending=False).head()
        rebounds_leaders_dfs = top_leaders_df[['player_name__player_name', 'total_rebounds']].sort_values(
            by='total_rebounds', ascending=False).head()
        assist_leaders_dfs = top_leaders_df[['player_name__player_name', 'assists']].sort_values(by='assists',
                                                                                                 ascending=False).head()
        blocks_leaders_dfs = top_leaders_df[['player_name__player_name', 'blocks']].sort_values(by='blocks',
                                                                                                ascending=False).head()
        efficiency_leaders_dfs = top_leaders_df[['player_name__player_name', 'efficiency']].sort_values(by='efficiency',
                                                                                                        ascending=False).head()

        # Calculate top leaders game stats
        points_leaders_by_averages = mean_df[['player_name__player_name', 'points']].sort_values(by='points', ascending=False)

        # Preparing player standings data
        accumulated_player_points = top_leaders_df.groupby(['player_name__player_name'])['points'].sum().reset_index()
        accumulated_player_points['games_played'] = top_leaders_df.groupby(['player_name__player_name'])['points'].count().reset_index(drop=True)


        accumulated_player_points = accumulated_player_points.sort_values(by='points', ascending=False)
        player_standings_data = accumulated_player_points.rename(columns={'points': 'points_scored'}).to_dict('records')


        # Players Average Age and Height
        average_age_height = pd.DataFrame(players.values('player_name','height'))

        average_age_height['height'] = average_age_height['height'].apply(pd.to_numeric, errors='coerce')

        # Calculate mean values for all players
        mean_height = average_age_height['height'].mean()




        for player in players:
            player.age = calculate_age(player.player_age)  # Call calculate_age function

        # Calculate the mean of the converted ages
        total_age = sum(player.age for player in players)
        player_count = len(players)
        mean_age = total_age / player_count if player_count > 0 else 0

        context = {
            'organizer': organizer,
            'competitions': competitions,
            'competitions_with_dates': competitions_with_dates,
            'teams': teams,
            'players': list(players),  # Converting QuerySet to list for better readability
            'player_stats': player_stats,
            'standings': standings_data,
            'player_standings': player_standings_data,

            # Mean stats
            'top_5_points': top_5_points.to_dict('records'),
            'top_5_rebounds': top_5_rebounds.to_dict('records'),
            'top_5_assists': top_5_assists.to_dict('records'),
            'top_5_blocks': top_5_blocks.to_dict('records'),
            'top_5_efficiencies': top_5_efficiencies.to_dict('records'),

            # Top single games
            'top5_point_leaders': points_leaders_dfs.to_dict('records'),
            'rebounds_leaders_dfs': rebounds_leaders_dfs.to_dict('records'),
            'assist_leaders_dfs': assist_leaders_dfs.to_dict('records'),
            'blocks_leaders_dfs': blocks_leaders_dfs.to_dict('records'),
            'efficiency_leaders_dfs': efficiency_leaders_dfs.to_dict('records'),

            # Average Leaders All Players
            'points_leaders_by_averages': points_leaders_by_averages.to_dict('records'),

            # Mean of Ages Heights
            'mean_height' : mean_height,
            'mean_age' : mean_age
        }

        return render(request, 'organizer_details.html', context)





# ORGANIZER UPDATE
class OrganizerUpdate(View):
    # Handle GET and POST requests to UPDATE ORGNIZER details
    def get(self, request, pk):
        update_organizer = get_object_or_404(Organizer, pk=pk)
        form = OrganizerForm(request.POST or None, instance=update_organizer)
        return render(request, 'update_organizer.html', {'form': form, 'update_organizer': update_organizer})

    def post(self, request, pk):
        update_organizer = get_object_or_404(Organizer, pk=pk)
        form = OrganizerForm(request.POST, request.FILES, instance=update_organizer)
        if form.is_valid():
            form.save()
            # Return a valid update message.
            messages.success(request, ("Organizer Updated Sucessfully ):"))
            return redirect('list-all-organizers')
            #return redirect('organizer-detail', pk=pk)
        return render(request, 'update_organizer.html', {'form': form, 'update_organizers': update_organizer})

# ORGANIZER DELETE
def delete_organizer(request, pk):
    organizer = get_object_or_404(Organizer, pk=pk)
    organizer.delete()
    # Return an 'invalid login' error message.
    messages.success(request, (" Organizer deleted successfully):"))
    return redirect('list-all-organizers')


########################################################################################################
###################################### COMPETITION #####################################################
########################################################################################################

# COMPETITION CREATION

class CompetitionCreate(CreateView):
    model = Competition
    form_class = CompetitionForm
    template_name = 'competitions_registration.html'
    success_url = '/list_all_organizers/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            competition_form = self.get_form()
            if competition_form.is_valid():
                messages.success(request, "Competition Registered Successfully :)")
                return self.form_valid(competition_form)

            else:
                return self.form_invalid(competition_form)
        return super().post(request, *args, **kwargs)


# LIST COMPETITIONS



# COMPETITION UPDATE
class CompetitionUpdateView(UpdateView):
    model = Competition
    form_class = CompetitionForm
    template_name = 'update_competition.html'
    success_url = reverse_lazy('list-all-organizers')

    def form_valid(self, form):
        messages.success(self.request, "Competition Updated Successfully :)")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


# DELETE COMPETITION
def delete_competition(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    competition.delete()
    # Return an 'invalid login' error message.
    messages.success(request, (" Competition deleted successfully):"))
    return redirect('list-all-organizers')
########################################################################################################
########################################################################################################
########################################################################################################
# TEAM CREATION VIEW
class TeamCreate(View):

    # GET FUNCTION TO FETCH THE TEAM REGISTRATION FORM
    def get(self, request):
        form = TeamForm()
        submitted = 'submitted' in request.GET
        return render(request, 'forms.html', {"form" : form, 'submitted': submitted})

    # POST FUNCTION TO POST OR SUBMIT  THE  REGISTERED TEAM
    def post(self, request):
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Team Added Successfully :)")
            return HttpResponseRedirect('/forms_db?submitted=True')
        return render(request, 'forms.html', {"form": form, 'submitted': False})

# LISTING ALL THE TEAMS VIEW
class TeamList(View):
    def get(self, request):
        teams = Team.objects.all()
        for team in teams:

            if not team.team_logo:
                team.team_logo = 'uploads/Team_Logos/default_logo.png'
        return render(request, 'list_all_teams.html', {'teams': teams})

#INDIVIDUAL TEAM VIEW
"""class TeamDetailView(DetailView):
    model = Team
    template_name = 'team_details.html'
    context_object_name = 'team_details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Call the base implementation to get the default context
        team_details = self.object # Retrieve the Team object for the given primary key (pk) from the URL
        team_images = BackgroundImages.objects.filter(team_pictures=team_details) # Query the BackgroundImages model for images related to the team
        players = team_details.players.all()    # Retrieve all players associated with the team using the related_name 'players' from the foreign key
        games = GameSchedule.objects.all()  # Query the GameSchedule model for all games
        #games = GameSchedule.objects.filter(team=team_details)

        # Add custom context to the context dictionary
        context.update({
            'team_images': team_images,  # Add team images to the context
            'games': games,  # Add all games to the context
            'players': players,  # Add players of the team to the context
            'timestamp': now().timestamp(),
            # Generate a unique timestamp to ensure that the browser loads the latest version of the .js file
        })

        # Return the updated context dictionary
        return context"""

#INDIVIDUAL TEAM VIEW

class TeamDetailView(View):
    def get(self, request, pk):
        team_details = get_object_or_404(Team, pk=pk)
        team_images = BackgroundImages.objects.filter(team_pictures=team_details)
        players = team_details.players.all()  # Using the foreign key Team related_name 'players'

        # Filter game schedules for the specific team
        games = GameSchedule.objects.filter(home_team=team_details) | GameSchedule.objects.filter(away_team=team_details)

        context = {
            'team_details': team_details,
            'team_images': team_images,
            'games': games,
            'players': players,
            'timestamp': now().timestamp(),
        }
        return render(request, 'team_details.html', context)












"""


class TeamListView(ListView):
    model = Team
    template_name = 'team_list.html'

class TeamDetailView(DetailView):
    model = Team
    template_name = 'team_detail.html'

class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'team_form.html'
    success_url = '/teams/'

class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'team_form.html'
    success_url = '/teams/'

"""


#TEAM UPDATE VIEW

class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'update_team.html'
    success_url = '/teams/'  # URL to redirect to after a successful update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PlayerFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = PlayerFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        update_teams = get_object_or_404(Team, pk=self.object.pk)
        form = self.get_form()  # Create a form instance with the POST data
        PlayerFormSet = inlineformset_factory(Team, Player, form=PlayerForm, extra=1, can_delete=False, max_num=13)
        formset = PlayerFormSet(request.POST, request.FILES, instance=update_teams)

        if form.is_valid() and formset.is_valid():  # Check if both the form and formset are valid
            form.save()  # Save the form if it's valid
            formset.save()  # Save the formset if it's valid
            messages.success(request, "Team and Players Updated Successfully :)")
            return redirect('teams-id', pk=self.object.pk)

        # Include formset in the context if there are errors
        return render(request, 'update_team.html', {'form': form, 'formset': formset, 'update_teams': update_teams})


#TEAM UPDATE VIEW
"""class TeamUpdate(View):
    # Handle GET and POST requests to UPDATE team details
    def get(self, request, pk):
        update_teams = get_object_or_404(Team, pk=pk)
        form = TeamForm(request.POST or None, instance=update_teams)
        return render(request, 'update_team.html', {'form': form, 'update_teams': update_teams})

    def post(self, request, pk):
        update_teams = get_object_or_404(Team, pk=pk)
        form = TeamForm(request.POST, request.FILES, instance=update_teams)
        PlayerFormSet = inlineformset_factory(Team, Player, form=PlayerForm, extra=1)

        if form.is_valid():
            form.save()
            formset = PlayerFormSet(request.POST, request.FILES, instance=update_teams)
            if formset.is_valid():
                formset.save()
                #messages.success(request, "Team and Players Added Successfully :)")
                return redirect('team-detail', pk=pk)

            # Return a valid update message.
            messages.success(request, (" Team Updated Sucessfully ):"))
            return redirect('team-detail', pk=pk)
        return render(request, 'update_team.html', {'form': form, 'update_teams': update_teams})"""




#TEAM DELETE
class TeamDelete(View):
    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        team.delete()
        # Return a 'delete' message.
        messages.success(request, (" Team deleted successfully):"))
        return redirect('list-all-teams')





###################################################################################################
################################ PLAYER VIEW ######################################################
###################################################################################################
# COMPETITION CREATION

class PlayerCreate(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'players_registration_form.html'
    success_url = '/list-all-players/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Player Registered Successfully :)")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print form errors to help diagnose the issue
        print(form.errors.as_text())
        messages.error(self.request, "There was an error registering the player. Please try again.")
        return super().form_invalid(form)



# LIST TEAM ROSTER

def team_roster(request, pk):
    teams_details = get_object_or_404(Team, pk=pk)
    players = teams_details.players.all()  # Using the foreign key Team related_name 'players'
    return render(request, 'team_roster.html', {'team_details': teams_details, 'players': players})

class PlayerDetail(View):
    def get(self, request, pk):
        player_details = get_object_or_404(Player, pk=pk)
        #player_images = BackgroundImages.objects.filter(player_image=player_details)

        context = {
            'player_details': player_details,
            #'player_images': player_images,
        }
        return render(request, 'player_details.html', context)


# UPDATE PLAYER
class PlayerUpdate(View):
    # Handle GET and POST requests to UPDATE ORGNIZER details
    def get(self, request, pk):
        update_player = get_object_or_404(Player, pk=pk)
        form = PlayerForm(request.POST or None, instance=update_player)
        return render(request, 'update_organizer.html', {'form': form, 'update_players': update_player})

    def post(self, request, pk):
        update_player = get_object_or_404(Organizer, pk=pk)
        form = PlayerForm(request.POST, request.FILES, instance=update_player)
        if form.is_valid():
            form.save()
            # Return a valid update message.
            messages.success(request, ("Player Updated Sucessfully ):"))
            return redirect('player_details')
            #return redirect('organizer-detail', pk=pk)
        return render(request, 'update_player.html', {'form': form, 'update_players': update_player})













########################################################################################################
########################################################################################################
########################################################################################################

##########################################################################
######################### API VIEWS #############################
###############################################################################

"""from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Competition, GameSchedule, 
from .serializers import CompetitionSerializer, GameScheduleSerializer

class CompetitionListAPI(APIView):
    def get(self, request, format=None):
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompetitionDetailAPI(APIView):
    def get_object(self, pk):
        return get_object_or_404(Competition, pk=pk)

    def get(self, request, pk, format=None):
        competition = self.get_object(pk)
        serializer = CompetitionSerializer(competition)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        competition = self.get_object(pk)
        serializer = CompetitionSerializer(competition, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        competition = self.get_object(pk)
        competition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GameScheduleListAPI(APIView):
    def get(self, request, format=None):
        games = GameSchedule.objects.all()
        serializer = GameScheduleSerializer(games, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GameScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameScheduleDetailAPI(APIView):
    def get_object(self, pk):
        return get_object_or_404(GameSchedule, pk=pk)

    def get(self, request, pk, format=None):
        game = self.get_object(pk)
        serializer = GameScheduleSerializer(game)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        game = self.get_object(pk)
        serializer = GameScheduleSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        game = self.get_object(pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""
