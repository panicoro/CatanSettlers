from django.urls import path
from catan import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('users/login/', views.AuthAPIView.as_view(), name='token_obtain_pair'),
    path('users/login/refresh/', TokenRefreshView.as_view(), name='refrescarToken'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
