# Generated by Django 5.1 on 2024-10-23 02:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B_Ball', '0011_organizer_competitions_alter_competition_organizers'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameschedule',
            name='competition_game_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_schedules', to='B_Ball.competition'),
        ),
    ]
