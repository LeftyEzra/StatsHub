# Generated by Django 5.1 on 2024-12-11 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('B_Ball', '0022_remove_organizer_competitions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]