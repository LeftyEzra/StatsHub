from django.test import TestCase

# Create your tests here.
from django.shortcuts import render, get_object_or_404
from .models import Player, PlayerStats
import pandas as pd

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    player_stats = PlayerStats.objects.filter(player_name=player)

    # Create a DataFrame from the queryset
    df = pd.DataFrame(player_stats.values('points', 'rebounds', 'assists', 'field_goal_attempts', 'field_goal_made', 'point_3_attempts', 'point_3_made', 'point_2_attempts', 'point_2_made', 'ft_attempts', 'ft_made', 'offensive_rebs', 'defensive_rebs', 'total_rebounds', 'blocks', 'steals', 'turnovers', 'personal_fouls', 'plus_minus', 'efficiency'))

    # Calculate averages
    averages = df.mean()

    context = {
        'player': player,
        'player_stats': player_stats,
        'averages': averages,
    }
    return render(request, 'player_detail.html', context)
