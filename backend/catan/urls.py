from django.urls import path
from catan import views

urlpatterns = [
    path('games/<int:pk>/player', views.PlayerInfo.as_view(),
         name='PlayerInfo'),
]
