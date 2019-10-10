from django.urls import path
from catan import views

urlpatterns = [
    path('games/<int:pk>/player', views.CardsList.as_view(), name='CardsList'),
]