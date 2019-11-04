from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from catan.views import *

urlpatterns = [
    # Rooms views
    path('rooms/', room_views.RoomList.as_view(), name='list_rooms'),
    path('rooms/<int:pk>/', room_views.RoomDetail.as_view(), name='join_room'),
    # Login/Register views
    path('users/login/', login_views.AuthAPIView.as_view(),
         name='tokenObtainPair'),
    path('users/login/refresh/', login_views.TokenRefreshView.as_view(),
         name='refreshToken'),
    path('users/', login_views.Register.as_view(),
         name='register'),
    # Players views
    path('games/<int:pk>/player/actions', players_views.PlayerActions.as_view(),
         name='PlayerActions'),
    path('games/<int:pk>/player', players_views.PlayerInfo.as_view(),
         name='PlayerInfo'),
    path('games/<int:pk>/', game_views.GameInfo.as_view(),
         name='GameInfo'),
    path('games/', game_views.GameList.as_view(), name='Games'),
    path('boards/', board_views.BoardList.as_view(), name='Boards'),
    path('games/<int:pk>/board/', board_views.BoardInfo.as_view(),
         name='BoardInfo'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
