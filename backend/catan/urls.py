from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from catan import views

urlpatterns = [
    path('rooms/', views.RoomList.as_view(), name='list_rooms'),
    path('rooms/<int:pk>/', views.RoomDetail.as_view(), name='join_room'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
