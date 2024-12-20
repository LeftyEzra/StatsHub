"""from django.test import TestCase

# Create your tests here.
from django.shortcuts import render, get_object_or_404
from .models import Player, PlayersStats
import pandas as pd

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    player_stats = PlayersStats.objects.filter(player_name=player)

    # Create a DataFrame from the queryset
    df = pd.DataFrame(player_stats.values('points', 'rebounds', 'assists', 'field_goal_attempts', 'field_goal_made', 'point_3_attempts', 'point_3_made', 'point_2_attempts', 'point_2_made', 'ft_attempts', 'ft_made', 'offensive_rebs', 'defensive_rebs', 'total_rebounds', 'blocks', 'steals', 'turnovers', 'personal_fouls', 'plus_minus', 'efficiency'))

    # Calculate averages and cumulative sum total
    averages = df.mean()
    cumsums  = df.cumsum()

    context = {
        'player': player,
        'player_stats': player_stats,
        'averages': averages,
        'cumsums' : cumsums,
    }
    return render(request, 'player_detail.html', context)"""


"""


### 1. **Using Django ORM Aggregation:**
Django's aggregation functions allow you to offload computations to the database, 
which is usually efficient for such operations.



def get_standings_with_games_played(competition_id):
    standings = Standing.objects.filter(competition_id=competition_id).annotate(
        games_played=F('games_won') + F('games_lost')
    ).order_by('-games_won', '-point_difference')
    return standings


### 2. **Using Pandas:
If you prefer working with Pandas for in-memory data manipulations,
 you can first retrieve data from the database and then process it using Pandas.


import pandas as pd
from .models import Competition, Standing

def get_standings_with_games_played(competition_id):
    standings_qs = Standing.objects.filter(competition_id=competition_id).values(
        'team__team_name', 'games_won', 'games_lost', 'points_scored', 'points_conceded',
        'points_scored_per_game', 'points_conceded_per_game', 'point_difference', 'expected_winning_percentage'
    )
    standings_df = pd.DataFrame.from_records(standings_qs)
    standings_df['games_played'] = standings_df['games_won'] + standings_df['games_lost']
    return standings_df


### 3. **Using NumPy:
NumPy is efficient for numerical computations, 
but you'd typically use it for arrays rather than Django QuerySets directly. 
However, you can combine it with Pandas or convert QuerySets to NumPy arrays.


import numpy as np
from .models import Competition, Standing

def get_standings_with_games_played(competition_id):
    standings_qs = Standing.objects.filter(competition_id=competition_id).values(
        'team__team_name', 'games_won', 'games_lost', 'points_scored', 'points_conceded',
        'points_scored_per_game', 'points_conceded_per_game', 'point_difference', 'expected_winning_percentage'
    )
    standings_df = pd.DataFrame.from_records(standings_qs)
    standings_df['games_played'] = np.sum([standings_df['games_won'], standings_df['games_lost']], axis=0)
    return standings_df


### 4. **Using Python's Built-in `sum()
For smaller datasets, you can simply use Python's built-in `sum()` function:
def get_standings_with_games_played(competition_id):
    standings = Standing.objects.filter(competition_id=competition_id)
    standings_data = []
    for standing in standings:
        games_played = standing.games_won + standing.games_lost
        standings_data.append({
            'team': standing.team.team_name,
            'games_played': games_played,
            'games_won': standing.games_won,
            'games_lost': standing.games_lost,
            'points_scored': standing.points_scored,
            'points_conceded': standing.points_conceded,
            'points_scored_per_game': standing.points_scored_per_game,
            'points_conceded_per_game': standing.points_conceded_per_game,
            'point_difference': standing.point_difference,
            'expected_winning_percentage': standing.expected_winning_percentage,
        })
    return standings_data
```

### Summary
- **Django ORM**: Use for direct database operations.
- **Pandas**: Use for complex in-memory data manipulations.
- **NumPy**: Use for large numerical arrays.
- **Python Built-in**: Use for simpler or smaller datasets.


"""


