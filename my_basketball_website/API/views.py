from django.shortcuts import render
from .serializers import TeamSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from B_Ball.models import  Team
#from .serializers import CompetitionSerializer, GameScheduleSerializer, Team

@api_view(['GET'])
def getData(request):
    language = {'name' : "python", 'purpose': 'RestFrame Work Tutorial with Insomia'}
    return Response(language)

class TeamListAPI(APIView):
    def get(self, request, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""class CompetitionListAPI(APIView):
    def get(self, request, format=None):
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompetitionDetailAPI(APIView):
    def get_object(self, pk):
        return get_object_or_404(Competition, pk=pk)

    def get(self, request, pk, format=None):
        competition = self.get_object(pk)
        serializer = CompetitionSerializer(competition)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        competition = self.get_object(pk)
        serializer = CompetitionSerializer(competition, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        competition = self.get_object(pk)
        competition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GameScheduleListAPI(APIView):
    def get(self, request, format=None):
        games = GameSchedule.objects.all()
        serializer = GameScheduleSerializer(games, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GameScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameScheduleDetailAPI(APIView):
    def get_object(self, pk):
        return get_object_or_404(GameSchedule, pk=pk)

    def get(self, request, pk, format=None):
        game = self.get_object(pk)
        serializer = GameScheduleSerializer(game)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        game = self.get_object(pk)
        serializer = GameScheduleSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        game = self.get_object(pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""



"""class CompetitionList(APIView):
    def get(self, request):
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data)

class GameScheduleList(APIView):
    def get(self, request):
        gameschedules = GameSchedule.objects.all()
        serializer = GameScheduleSerializer(gameschedules, many=True)
        return Response(serializer.data)"""
