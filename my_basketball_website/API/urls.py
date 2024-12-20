from django.urls import path
from . import views
from .views import TeamListAPI

urlpatterns = [
    path('data/', views.getData, name='api-data'),
    path('teamList/',TeamListAPI.as_view(), name='team-data'),
    #path('register_user', views.register_user, name='register-user'),


]