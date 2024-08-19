from django.urls import path
from . import views

urlpatterns = [


                path('', views.home, name='home'),
                #path('carousal', views.carousal, name='carousal'),
                #path('delete/<task_id>', views.delete, name='delete'),
                #path('update/<task_id>', views.update, name='update'),
                #path('complete/<task_id>', views.complete, name='complete'),
                path('about/', views.about, name='about'),
                path('stats_tables/', views.stats_tables, name='table'),

               ]