from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from catan import views

urlpatterns = [
    path('games/', views.GameList.as_view()),
    path('boards/', views.BoardList.as_view()),
    path('games/<int:pk>/board/', views.BoardInfo.as_view(),
         name='BoardInfo'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
