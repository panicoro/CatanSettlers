from django.contrib import admin
from django.urls import path, include
from backend.views import index

urlpatterns = [
    path('', include('catan.urls')),
    path('admin/', admin.site.urls),
    path('', index, name='index')
]
