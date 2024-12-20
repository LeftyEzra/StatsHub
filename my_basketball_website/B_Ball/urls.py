from django.urls import path
from . import views
from .views import OrganizerCreate, OrganizerUpdate
from .views import  CompetitionCreate, CompetitionUpdateView
from .views import OrganizerAndCompetitionList, about
from .views import OrganizerDetailView, GetGamesByDate, GetTopAverages
from .views import TeamCreate, TeamList, TeamDetailView, TeamDelete, TeamUpdateView
from .views import PlayerDetail,PlayerCreate, PlayerDetail, PlayerUpdate

#Api urls
#from .views import CompetitionListAPI, CompetitionDetailAPI, GameScheduleListAPI, GameScheduleDetailAPI

urlpatterns = [
                #Extras
                path('', views.home, name='home'),
                path('search_team/', views.search_teams_players, name='search-teams-players'),
                path('about/', views.about, name='about'),
                path('about_registration/', views.about_registration, name='about-registration'),

                # Organizers
                path('create_organizer/', OrganizerCreate.as_view(), name='create-organizer'),
                path('list_all_organizers/', OrganizerAndCompetitionList.as_view(), name='list-all-organizers'),
                path('organizers/<int:pk>/', OrganizerDetailView.as_view(), name='organizer-id'),
                path('organizers/<int:competition_id>/games/<str:date>/', GetGamesByDate.as_view(), name='games-by-date'),
                path('top_averages/<int:competition_id>/', GetTopAverages.as_view(), name='top-averages'),
                path('update_organizer/<int:pk>/',OrganizerUpdate.as_view(), name='update-organizer'),
                path('delete_organizer/<int:pk>/',views.delete_organizer, name='delete-organizer'),


                ##Competion Urls
                path('create_competition/', CompetitionCreate.as_view() , name='new-competition'),
                #path('competition/<int:pk>/', CompetitionDetailView.as_view(), name='competition-id'),
                path('update-competition/<int:pk>/', CompetitionUpdateView.as_view(), name='update-competition'),
                path('delete-competition/<int:pk>/', views.delete_competition, name='delete-competition'),

                # Teams urls
                # CBV Path for Team creation, listing, update and delete.
                path('forms_db/', TeamCreate.as_view(), name='forms-db'),
                path('list_all_teams', TeamList.as_view(), name='list-all-teams'),
                path('teams_id/<int:pk>/', TeamDetailView.as_view(), name='teams-id'),
                path('delete_team/<int:pk>/', TeamDelete.as_view(), name='delete-team'),
                path('update_team/<int:pk>/', TeamUpdateView.as_view(), name='update-team'),

                # Players urls
                path('register_players/', PlayerCreate.as_view(), name='create-player'),
                path('team_roster/<int:pk>/', views.team_roster, name='team-roster'),
                path('player_id/<int:pk>/', PlayerDetail.as_view(), name='player-id'),


                #ath('update_player/<int:pk>/', views.PlayerUpdate, name='update-player'),
                #path('delete_player/<int:pk>/', views.delete_player, name='team-roster'),

                # path('competitions/<int:competition_pk>/teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
                # path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'




                # Path for viewing, updating, and deleting a specific team
                #path('teams_id/<int:pk>/', TeamDetail.as_view(), name='team-detail'),

                #path('forms_db/', views.forms_db, name='forms-db'),
                #path('list_all_teams', views.list_all_teams, name='list-all-teams'),
                #path('teams_id/<int:pk>/', views.teams_id, name='teams-id'),
                #path('update_team/<int:pk>/', views.update_team, name='update-team'),
                #path('delete_team/<int:pk>/', views.delete_team, name='delete-team'),
                #path('team_roster/<int:pk>/', views.team_roster, name='team-roster'),

                #Players
                path('stats_tables/<int:game_pk>', views.stats_tables, name='table'),


                #Games urls
                path('game_schedule/', views.game_schedule, name='game-schedule'),
                path('game_summary/<int:pk>/', views.game_summary, name='game-summary'),






                #Api url paths
                #path('api/competitions/', CompetitionListAPI.as_view(), name='competition-list'),
                #path('api/competitions/<int:pk>/', CompetitionDetailAPI.as_view(), name='competition-detail'),
                #path('api/games/', GameScheduleListAPI.as_view(), name='game-schedule-list'),
                #path('api/games/<int:pk>/', GameScheduleDetailAPI.as_view(), name='game-schedule-detail'),




               ]


"""

from django.urls import path
from .views import TeamCreate, TeamDetail, TeamList, TeamUpdate

urlpatterns = [
    path('teams/', TeamList.as_view(), name='list-all-teams'),
    path('teams/<int:pk>/', TeamDetail.as_view(), name='team-detail'),
    path('teams/update/<int:pk>/', TeamUpdate.as_view(), name='update-team'),
    path('teams/create/', TeamCreate.as_view(), name='team-create'),
]




"""





