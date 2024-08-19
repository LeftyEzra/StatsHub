# Generated by Django 5.1 on 2024-08-18 23:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B_Ball', '0002_team_alter_backgroundimages_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('home_team_scores', models.PositiveIntegerField(default=0)),
                ('away_team_scores', models.PositiveIntegerField(default=0)),
                ('highlight_moments', models.CharField(max_length=500)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='B_Ball.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='B_Ball.team')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jersey_numbers', models.IntegerField(default=0)),
                ('player_name', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=10)),
                ('height', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
                ('player_image', models.ImageField(upload_to='uploads/Players_images/')),
                ('team', models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='B_Ball.team')),
            ],
        ),
    ]
