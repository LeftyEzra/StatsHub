from django.contrib import admin
from .models import BackgroundImages
from .models import Team
from .models import Game
from .models import Player
from .models import PlayersStats
from .models import QuarterlyScores

# Register your models here.

# Image Uploads
admin.site.register(BackgroundImages)
admin.site.register(Team)

# Admin REgistration for Game model.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('date', 'home_team', 'away_team', 'home_team_scores','away_team_scores', 'highlight_moments')
    ordering = ("date",)
    search_fields = ('date',)
    search_help_text = ('home_team', 'away_team',)


# Player Model
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('jersey_numbers', 'player_image', 'player_name', 'position', 'height', 'weight', 'team')
    ordering = ("jersey_numbers",)
    search_fields = ('player_name', 'position', 'team',)
    search_help_text = ('player_name', 'position', 'team',)


@admin.register(PlayersStats)
class PlayersStatsAdmin(admin.ModelAdmin):
    list_display = ( 'player_name','player_team','game','minutes','points','field_goal_attempts',
                    'field_goal_made','fg_percent','point_3_attempts','point_3_made',
                    'point_3_percent','point_2_attempts','point_2_made','point_2_percent','ft_attempts','ft_made','ft_percent',
                    'offensive_rebs','defensive_rebs','total_rebounds','blocks', 'assists',
                    'steals','turnovers','personal_fouls','plus_minus','efficiency')
    #list_filter = ('event_date', 'venue')
    ordering = ('player_name',)
    search_fields = ('player_name','jersey_numbers','player_team')
    search_help_text = ('player_name','player_team')



@admin.register(QuarterlyScores)
class QuarterlyScoresAdmin(admin.ModelAdmin):
    list_display = ('game', 'home_team_quarter_1', 'home_team_quarter_2', 'home_team_quarter_3', 'home_team_quarter_4',
                    'away_team_quarter_1','away_team_quarter_2','away_team_quarter_3','away_team_quarter_4',)
    #list_filter = ('event_date', 'venue')
    #ordering = ("jersey_numbers",)
    #search_fields = ('player_name','jersey_numbers')
    #search_help_text = ('player_name',)
