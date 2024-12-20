# This serializer.py files is a translator between complex data types,
# like django models and simple data fotmat like JSON or XML.
# The purpose is to convert python datatypes into JSON, XML or other content datatypes.
# Also convert parsed data back into complex data types, after cross checking and validating the incoming data.

import sys
sys.path.append('C:/BASKETBALL/my_basketball_website')

from rest_framework import serializers
from B_Ball.models import Team

# Creating a competion serializer
"""class CompetitionSerializer(serializers.ModelSerializer):
    class Meta: # Defines the model and fields that should be included.
        model = Competition
        fields = '__all__'



# Creating a Game Schedule serializer

class GameScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSchedule
        fields = '__all__'"""


# Creating a competion serializer
class TeamSerializer(serializers.ModelSerializer):
    class Meta: # Defines the model and fields that should be included.
        model = Team
        fields = '__all__'