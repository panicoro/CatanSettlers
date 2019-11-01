from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from catan import views

urlpatterns = [
    path('rooms/', views.RoomList.as_view(), name='list_rooms'),
    path('rooms/<int:pk>/', views.RoomDetail.as_view(), name='join_room'),
    path('users/login/', views.AuthAPIView.as_view(),
         name='tokenObtainPair'),
    path('users/login/refresh/', TokenRefreshView.as_view(),
         name='refreshToken'),
    path('users/', views.Register.as_view(),
         name='register'),
    path('games/<int:pk>/player', views.PlayerInfo.as_view(),
         name='PlayerInfo'),
    path('games/<int:pk>/', views.GameInfo.as_view(),
         name='GameInfo'),
    path('games/', views.GameList.as_view(), name='Games'),
    path('boards/', views.BoardList.as_view(), name='Boards'),
    path('games/<int:pk>/board/', views.BoardInfo.as_view(),
         name='BoardInfo'),
    path('games/<int:pk>/player/actions/', views.PlayerActions.as_view(),
         name='PlayerActions'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
