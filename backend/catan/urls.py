from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from catan import views

urlpatterns = [
    path('', views.lista_tablero),
    path('hexagonos/', views.lista_hexagono),
]

urlpatterns = format_suffix_patterns(urlpatterns)