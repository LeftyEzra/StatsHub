from django.contrib import admin
from .models import BackgroundImages
from .models import Competition
from .models import Team
from .models import GameSchedule
from .models import Player
from .models import PlayersStats
from .models import QuarterlyScores
from .models import Organizer
from .models import Standing

# Register your models here.

# Image Uploads
admin.site.register(BackgroundImages)
#admin.site.register(Organizer)

# Inline models for nested editing
class TeamInline(admin.TabularInline):
    # This inline model represents the 'teams' field on the Competition model
    # The 'through' attribute points to the intermediate table created by the ManyToMany relationship
    model = Competition.teams.through
    extra = 1 # Adds an extra empty form for additional team entries by default

class CompetitionInline(admin.TabularInline):
    model = Organizer.competitions.through
    extra = 1

class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1

class BackgroundImageInline(admin.TabularInline):
    model = BackgroundImages
    extra = 1

# Admin classes with inlines
@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizer_logo', 'contact_info')
    search_fields = ('name', )
    #inlines = [CompetitionInline]

    def get_competitions(self, obj):
        # Get all the competitions and seperate them with commas
        return ", ".join([competition.name for competition in obj.competitions.all()])
    get_competitions.short_description = 'Competitions' # Renaming the  column header name for the get_competitions


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'get_organizers', 'location', 'start_date', 'end_date', 'get_teams')
    search_fields = ('name', 'location', 'organizers__name', 'year')
    ordering = ('start_date',)
    inlines = [TeamInline]  # Includes inline editing for teams in the competition admin panel
    filter_horizontal = ('teams', 'organizers')  # Easier selection of teams and organizers

    def get_teams(self, obj):
        if obj.teams:
            return ", ".join([team.team_name for team in obj.teams.all()])
        return "No teams"
    get_teams.short_description = 'Teams'

    def get_organizers(self, obj):
        if obj.organizers:
            return ", ".join([organizer.name for organizer in obj.organizers.all()])
        return "No organizers"
    get_organizers.short_description = 'Organizers'



@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [PlayerInline, BackgroundImageInline]
    list_display = ('team_name', 'team_logo', 'team_abbreviation', 'team_head_coach',
                    'get_players', 'get_images','city', 'founded','country')
    ordering = ('team_name',)
    search_fields = ('team_name', 'team_abbreviation', 'players__player_name')

    def get_players(self, obj):
        return ", ".join([player.player_name for player in obj.players.all()])
    get_players.short_description = 'Players'

    def get_images(self, obj):
        return ", ".join([image.image_captions for image in obj.team_pictures.all()])
    get_images.short_description = 'Background Images'

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    inlines = [BackgroundImageInline]
    list_display = ('jersey_numbers', 'player_image', 'player_name', 'player_age', 'position', 'height', 'weight', 'get_teams', 'player_club', 'get_players_images')
    ordering = ('team_name__team_name',)
    search_fields = ('player_name', 'position', 'team_name__team_name')

    def get_teams(self, obj):
        return obj.team_name.team_name if obj.team_name else "No Team"
    get_teams.short_description = 'Teams'

    def get_players_images(self, obj):
        return ", ".join([image.image_captions for image in obj.player_pictures.all()])


# Admin REgistration for Game model.
@admin.register(GameSchedule)
class GameScheduleAdmin(admin.ModelAdmin):
    list_display = ('date','competition_game_schedule', 'home_team', 'away_team', 'home_team_scores','away_team_scores', 'highlight_moments')
    ordering = ("-date",)
    search_fields = ('date',)
    search_help_text = ('home_team', 'away_team',)





@admin.register(PlayersStats)
class PlayersStatsAdmin(admin.ModelAdmin):
    list_display = ( 'player_name','player_team','minutes','points','field_goal_attempts',
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
    ordering = ("game",)
    #search_fields = ('player_name','jersey_numbers')
    #search_help_text = ('player_name',)"""




@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ('team','competition','games_won','games_lost',
                       )
    list_filter = ('team',)
    ordering = ("games_won",)
    search_fields = ('team',)
    #search_help_text = ('player_name',)"""
