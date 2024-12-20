# Generated by Django 5.1 on 2024-11-13 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B_Ball', '0014_player_player_country_team_city_team_country_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standing',
            old_name='point_difference',
            new_name='game_win_loss_percent',
        ),
        migrations.RemoveField(
            model_name='player',
            name='player_country',
        ),
        migrations.AddField(
            model_name='standing',
            name='games_played',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='standing',
            name='point_difference_per_game',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='standing',
            name='points_diff',
            field=models.IntegerField(default=0),
        ),
    ]
