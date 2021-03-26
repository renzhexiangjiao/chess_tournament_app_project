from django.urls import path
from chess import views

app_name = 'chess'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('play/', views.PlayView.as_view(), name='play'),
    path('moveupdate/', views.MoveUpdateView.as_view(), name='moveupdate'),
    path('movelist/', views.MoveListView.as_view(), name='movelist'),
]