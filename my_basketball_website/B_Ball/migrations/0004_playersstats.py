# Generated by Django 5.1 on 2024-08-18 23:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B_Ball', '0003_game_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayersStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes', models.CharField(default=0, max_length=5)),
                ('points', models.PositiveIntegerField()),
                ('field_goal_attempts', models.IntegerField(default=0)),
                ('field_goal_made', models.IntegerField(default=0)),
                ('fg_percent', models.CharField(db_default=0, default=0, max_length=10)),
                ('point_3_attempts', models.IntegerField(default=0)),
                ('point_3_made', models.IntegerField(default=0)),
                ('point_3_percent', models.CharField(default=0, max_length=10)),
                ('point_2_attempts', models.IntegerField(default=0)),
                ('point_2_made', models.IntegerField(default=0)),
                ('point_2_percent', models.CharField(db_default=0, default=0, max_length=10)),
                ('ft_attempts', models.IntegerField(default=0)),
                ('ft_made', models.IntegerField(default=0)),
                ('ft_percent', models.CharField(db_default=0, default=0, max_length=10)),
                ('offensive_rebs', models.IntegerField(default=0)),
                ('defensive_rebs', models.IntegerField(default=0)),
                ('total_rebounds', models.IntegerField(default=0)),
                ('blocks', models.IntegerField(default=0)),
                ('assists', models.IntegerField(default=0)),
                ('steals', models.IntegerField(default=0)),
                ('turnovers', models.IntegerField(default=0)),
                ('personal_fouls', models.IntegerField(default=0)),
                ('plus_minus', models.CharField(max_length=5)),
                ('efficiency', models.CharField(max_length=5)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='B_Ball.game')),
                ('player_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='B_Ball.player')),
                ('player_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='B_Ball.team')),
            ],
        ),
    ]