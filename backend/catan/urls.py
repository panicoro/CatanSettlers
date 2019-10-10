from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from catan import views

urlpatterns = [
    path('boards/', views.list_board),
    path('boards/<int:pk>/', views.board_detail),
    path('games/', views.list_game),
    path('games/<int:pk>/', views.game_detail),
    path('hexes/', views.list_hexes),
]

urlpatterns = format_suffix_patterns(urlpatterns)