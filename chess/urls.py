from django.urls import path
from chess import views

app_name = 'chess'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('play/', views.PlayLobbyView.as_view(), name='playlobby'),
    path('play/<int:game_id>/', views.PlayView.as_view(), name='play'),
    path('play/spectate/<int:game_id>/', views.PlayView.as_view(), name='spectate'),
    path('moveupdate/<int:game_id>/', views.MoveUpdateView.as_view(), name='moveupdate'),
    path('movelist/<int:game_id>/', views.MoveListView.as_view(), name='movelist'),
    path('game-history/<int:game_id>/', views.GameHistoryView.as_view(), name='gamehistory'),
    path('board-history/<int:game_id>/', views.BoardHistoryView.as_view(), name='boardhistory'),
    path('tournament-history/', views.show_tournament_history, name='history'),
    path('tournament/<tournament_name>/', 
         views.show_tournament, name='show_tournament'),
    path('calendar/', views.show_calendar, name='calendar'),
    path('update-calendar/', views.CalendarUpdateView.as_view(), name='updatecalendar'),
    path('accountpage/', views.show_accountpage, name='accountpage'),
    path('accountpage/create/', views.create_accountpage, name='create_accountpage'),
    path('add_tournament/', views.add_tournament, name='add_tournament'),
    path('delete-tournament/', views.DeleteTournamentView.as_view(), name='deletetournament'),
    path('tournament-signup/', views.TournamentSignupView.as_view(), name='tournamentsignup'),
]