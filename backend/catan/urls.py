from django.urls import path
from catan.views import *

urlpatterns = [
    path('games/<int:pk>/player', ResourceList.as_view())
    #path('game', GameList.as_view()),
]