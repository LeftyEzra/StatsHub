from django.db import models
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum




# Create your models here.


class Organizer(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField(blank=True, null=True)
    organizer_logo = models.ImageField(upload_to='uploads/Organizer_Logos/', blank=True, null=True)

    def __str__(self):
        return self.name





# Model for team/nation
class Team(models.Model):
    team_name = models.CharField(max_length=100, blank=False, null=False)
    team_abbreviation = models.CharField(max_length=100, blank=False, null=False)
    team_logo = models.ImageField(upload_to='uploads/Team_Logos/',blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    team_head_coach = models.CharField(max_length=100,blank=True, null=True)
    head_coach_photo = models.ImageField(upload_to='uploads/Coaches/',blank=True, null=True)
    team_assitance_coach1 = models.CharField(max_length=100,blank=True, null=True)
    assitance_coach1_photo = models.ImageField(upload_to='uploads/Coaches/',blank=True, null=True)
    team_assitance_coach2 = models.CharField(max_length=100,blank=True, null=True)
    assitance_coach2_photo = models.ImageField(upload_to='uploads/Coaches/',blank=True, null=True)
    founded = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100,blank=True, null=True)


    def __str__(self):
        return f'{self.team_name}'

    class Meta:
        verbose_name_plural = 'Teams' # Instructing django to properly pluralize Categorys in the database



class Competition(models.Model):
    year = models.CharField(max_length=4, default='2024')
    name = models.CharField(max_length=255)
    organizers = models.ManyToManyField(Organizer, related_name='competitions', blank=True, )
    teams = models.ManyToManyField(Team)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=255,)
    description = models.TextField(blank=True, null=True)



    def __str__(self):
        return self.name



# Game models
class GameSchedule(models.Model):
    date = models.DateField(default=timezone.now)
    home_team = models.ForeignKey(Team, related_name= 'home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.CASCADE)
    home_team_scores = models.PositiveIntegerField(blank=True, null=True)
    away_team_scores = models.PositiveIntegerField(blank=True, null=True)
    highlight_moments = models.CharField(max_length=500)
    competition_game_schedule = models.ForeignKey(Competition, related_name='game_schedules', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.date)#.strftime('%Y-%m-%d')




class Standing(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # Foriegn relationship with Team
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)  # Foriegn relationship with Competition
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    game_schedule = models.ForeignKey(GameSchedule, on_delete=models.CASCADE, related_name='standings', null=True,blank=True)

    """@property
    def total_points_scored(self):
        home_scores = GameSchedule.objects.filter(home_team=self.team, competition_game_schedule=self.competition).aggregate(Sum('home_team_scores'))['home_team_scores__sum'] or 0
        away_scores = GameSchedule.objects.filter(away_team=self.team, competition_game_schedule=self.competition).aggregate(Sum('away_team_scores'))['away_team_scores__sum'] or 0
        return home_scores + away_scores

    @property
    def total_points_conceded(self):
        home_conceded = GameSchedule.objects.filter(home_team=self.team, competition_game_schedule=self.competition).aggregate( Sum('away_team_scores'))['away_team_scores__sum'] or 0
        away_conceded =  GameSchedule.objects.filter(away_team=self.team, competition_game_schedule=self.competition).aggregate(Sum('home_team_scores'))['home_team_scores__sum'] or 0
        return home_conceded + away_conceded"""

    def __str__(self):
        return f"{self.team} - {self.competition.name} Standing"





# Players model
class Player(models.Model):
    jersey_numbers = models.PositiveIntegerField()
    player_name = models.CharField(max_length=50, blank=False, null=False)
    player_age = models.DateField()
    position = models.CharField(max_length=30,blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    weight = models.CharField(blank=True, null=True)
    player_image = models.ImageField(upload_to='uploads/Players_images/',blank=True, null=True)
    player_club = models.CharField(max_length=50,blank=True, null=True)
    team_name = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE,blank=True, null=True)


    def __str__(self):
        return self.player_name






# Pl,ayers Average Stats model
class PlayersStats(models.Model):
    player_name = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    minutes = models.CharField(max_length=5,)
    points = models.PositiveIntegerField()
    field_goal_attempts = models.PositiveIntegerField()
    field_goal_made = models.PositiveIntegerField()
    fg_percent = models.CharField(max_length=10)
    point_3_attempts = models.PositiveIntegerField()
    point_3_made = models.PositiveIntegerField()
    point_3_percent = models.CharField(max_length=10)
    point_2_attempts = models.PositiveIntegerField()
    point_2_made = models.PositiveIntegerField()
    point_2_percent = models.CharField(max_length=10)
    ft_attempts = models.PositiveIntegerField()
    ft_made = models.PositiveIntegerField()
    ft_percent = models.CharField(max_length=10)
    offensive_rebs = models.PositiveIntegerField()
    defensive_rebs = models.PositiveIntegerField()
    total_rebounds = models.PositiveIntegerField()
    blocks = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    steals = models.PositiveIntegerField()
    turnovers = models.PositiveIntegerField()
    personal_fouls = models.PositiveIntegerField()
    plus_minus = models.CharField(max_length=5)
    efficiency = models.CharField(max_length=5)




    def __str__(self):
        return f'{self.player_name}'


    class Meta:
        verbose_name_plural = 'Players Stats'



# Quarterly Scores
class QuarterlyScores(models.Model):
    game = models.ForeignKey(GameSchedule, on_delete=models.CASCADE)
    home_team_quarter_1 = models.PositiveIntegerField()
    home_team_quarter_2 = models.PositiveIntegerField()
    home_team_quarter_3 = models.PositiveIntegerField()
    home_team_quarter_4 = models.PositiveIntegerField()
    away_team_quarter_1 = models.PositiveIntegerField()
    away_team_quarter_2 = models.PositiveIntegerField()
    away_team_quarter_3 = models.PositiveIntegerField()
    away_team_quarter_4 = models.PositiveIntegerField()


    def __str__(self):
        return f'{self.game}'


    class Meta:
        verbose_name_plural = 'Quarterly Scores'



# Background Images
class BackgroundImages(models.Model):
    image_captions = models.CharField(max_length=20, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/action_images/')  # This will automatically create a folder in the project directory.
    team_pictures = models.ForeignKey(Team, related_name='team_pictures', on_delete=models.CASCADE, blank=True, null=True)
    player_pictures = models.ForeignKey(Player, related_name='player_pictures', on_delete=models.CASCADE, blank=True, null=True)
    competition_pictures = models.ForeignKey(Competition, related_name='competition_pictures', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.image_captions

    class Meta:
        verbose_name_plural = 'Background Images'




"""
class Team(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='team_logos/')
    league = models.CharField(max_length=255)
    founded = models.IntegerField()
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

class Standing(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)  # Ensures each team has a unique standing record
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    points_scored = models.IntegerField(default=0)
    points_conceded = models.IntegerField(default=0)
    points_scored_per_game = models.FloatField(default=0.0)
    points_conceded_per_game = models.FloatField(default=0.0)
    point_difference = models.FloatField(default=0.0)
    expected_winning_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.team.name} Standing"





from django.db import models
from django.utils import timezone

class Organizer(models.Model):
    # Assuming fields for Organizer as you have them defined
    pass

class Team(models.Model):
    team_name = models.CharField(max_length=100, blank=False, null=False)
    team_abbreviation = models.CharField(max_length=100, blank=False, null=False)
    team_logo = models.ImageField(upload_to='uploads/Team_Logos/', blank=True, null=True)
    team_head_coach = models.CharField(max_length=100, blank=True, null=True)
    head_coach_photo = models.ImageField(upload_to='uploads/Coaches/', blank=True, null=True)
    team_assitance_coach1 = models.CharField(max_length=100, blank=True, null=True)
    assitance_coach1_photo = models.ImageField(upload_to='uploads/Coaches/', blank=True, null=True)
    team_assitance_coach2 = models.CharField(max_length=100, blank=True, null=True)
    assitance_coach2_photo = models.ImageField(upload_to='uploads/Coaches/', blank=True, null=True)

class Competition(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    organizers = models.ManyToManyField(Organizer, related_name='competitions_set')
    teams = models.ManyToManyField(Team)
    year = models.CharField(max_length=4, default='2024')

class Standing(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # Many-to-One relationship with Team
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)  # Many-to-One relationship with Competition
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    points_scored = models.IntegerField(default=0)
    points_conceded = models.IntegerField(default=0)
    points_scored_per_game = models.FloatField(default=0.0)
    points_conceded_per_game = models.FloatField(default=0.0)
    point_difference = models.FloatField(default=0.0)
    expected_winning_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.team.team_name} - {self.competition.name} Standing"









"""