# Generated by Django 5.1 on 2024-08-25 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B_Ball', '0006_backgroundimages_competition_pictures_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='assitance_coach1_photo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/Coaches/'),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_logo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/Team_Logos/'),
        ),
    ]
