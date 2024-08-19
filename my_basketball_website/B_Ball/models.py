from django.db import models
from datetime import datetime


# Create your models here.

#Background Images
class BackgroundImages(models.Model):
    image_captions = models.CharField(max_length=20,default='',blank=True,null=True)
    image = models.ImageField(upload_to='uploads/action_images/') #This will automatically create a folder in the project directory.

    def __str__(self):
        return self.image_captions

        # Instructing django to properly pluralize Categorys in the database

    class Meta:
        verbose_name_plural = 'Background Images'






# Model for team/nation
class Team(models.Model):
    team_name = models.CharField(max_length=50, blank=False, null=False)
    #player_name = models.ForeignKey('Player',max_length=50,default='A', blank=False, null=False, on_delete=models.CASCADE, related_name='teams')
    team_abbreviation = models.CharField(max_length=50, blank=False, null=False)
    team_logo = models.ImageField(upload_to='uploads/Team_Logos/')

    def __str__(self):
        return f'{self.team_name}'

        # Instructing django to properly pluralize Categorys in the database

    class Meta:
        verbose_name_plural = 'Teams'




# Game models
class Game(models.Model):
    date = models.DateField()
    home_team = models.ForeignKey(Team, related_name= 'home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.CASCADE)
    home_team_scores = models.PositiveIntegerField(default=0)
    away_team_scores = models.PositiveIntegerField(default=0)
    highlight_moments = models.CharField(max_length=500)

    def __str__(self):
        return str(self.date)#.strftime('%Y-%m-%d')






# Players model
class Player(models.Model):
    jersey_numbers = models.IntegerField(default=0)
    player_name = models.CharField(max_length=50, blank=False, null=False)
    position = models.CharField(max_length=10)
    height = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    team = models.ForeignKey(Team, max_length=50, blank=False, null=False, on_delete=models.CASCADE, )
    player_image = models.ImageField(upload_to='uploads/Players_images/')

    def __str__(self):
        return self.player_name


# Pl,ayers Average Stats model
class PlayersStats(models.Model):
    player_name = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    minutes = models.CharField(max_length=5, default=0)
    points = models.PositiveIntegerField()
    field_goal_attempts = models.IntegerField(default=0)
    field_goal_made = models.IntegerField(default=0)
    fg_percent = models.CharField(default=0, db_default=0, max_length=10)
    point_3_attempts = models.IntegerField(default=0)
    point_3_made = models.IntegerField(default=0)
    point_3_percent = models.CharField(default=0, max_length=10)
    point_2_attempts = models.IntegerField(default=0)
    point_2_made = models.IntegerField(default=0)
    point_2_percent = models.CharField(default=0, db_default=0, max_length=10)
    ft_attempts = models.IntegerField(default=0)
    ft_made = models.IntegerField(default=0)
    ft_percent = models.CharField(default=0, db_default=0, max_length=10)
    offensive_rebs = models.IntegerField(default=0)
    defensive_rebs = models.IntegerField(default=0)
    total_rebounds = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    steals = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)
    personal_fouls = models.IntegerField(default=0)
    plus_minus = models.CharField(max_length=5)
    efficiency = models.CharField(max_length=5)



    def __str__(self):
        return f'{self.player_name}'


    class Meta:
        verbose_name_plural = 'Players Stats'



# Quarterly Scores
class QuarterlyScores(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    home_team_quarter_1 = models.PositiveIntegerField(default=0)
    home_team_quarter_2 = models.PositiveIntegerField(default=0)
    home_team_quarter_3 = models.PositiveIntegerField(default=0)
    home_team_quarter_4 = models.PositiveIntegerField(default=0)
    away_team_quarter_1 = models.PositiveIntegerField(default=0)
    away_team_quarter_2 = models.PositiveIntegerField(default=0)
    away_team_quarter_3 = models.PositiveIntegerField(default=0)
    away_team_quarter_4 = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f'{self.game}'








