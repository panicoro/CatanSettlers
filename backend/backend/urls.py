from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('catan.urls')),
    path('admin/', admin.site.urls),
    path('', include('catan.urls')),
]
