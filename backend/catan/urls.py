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
]

urlpatterns = format_suffix_patterns(urlpatterns)
