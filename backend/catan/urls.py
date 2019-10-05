from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from catan import views

urlpatterns = [
    path('rooms/', views.RoomList.as_view()),
    path('rooms/<int:pk>/', views.RoomDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
