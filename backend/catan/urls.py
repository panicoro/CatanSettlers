from django.urls import path
from catan import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('users/login/', views.AuthAPIView.as_view(),
         name='tokenObtainPair'),
    path('users/login/refresh/', TokenRefreshView.as_view(),
         name='refreshToken'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
