from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
#from ..models import Competition, GameSchedule,
#from .serializers import CompetitionSerializer, GameScheduleSerializer

@api_view(['GET'])
def getData(request):
    language = {'name' : "python", 'purpose': 'RestFrame Work Tutorial'}
    return Response(language)
