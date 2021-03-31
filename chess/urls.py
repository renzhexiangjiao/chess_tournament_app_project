from django.urls import path
from chess import views

app_name = 'chess'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tournament-history/', views.show_tournament_history, name='history'),
    path('tournament/<tournament_name>/', 
         views.show_tournament, name='show_tournament'),
    path('calendar/', views.show_calendar, name='calendar'),
]