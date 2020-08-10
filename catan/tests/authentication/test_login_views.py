import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenRefreshView
from catan.views.login_views import AuthAPIView
from django.urls import reverse


@pytest.mark.django_db
class TestViews:
    def test_AuthAPIView_200(self):
        username = 'prueba'
        email = 'prueba@test.com'
        password = 'prueba'
        User.objects.create_user(username, email, password)
        path = reverse('tokenObtainPair')
        data = {'user': username, 'pass': password}
        path = reverse('tokenObtainPair')
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        view = AuthAPIView.as_view()
        response = view(request)
        refresh = response.data['refresh']
        pathRefresh = reverse('refreshToken')
        dataRefresh = {'refresh': refresh}
        requestRefresh = RequestFactory().post(pathRefresh, dataRefresh,
                                               content_type='application/json')
        viewRefresh = TokenRefreshView.as_view()
        responseRefresh = viewRefresh(requestRefresh)
        assert responseRefresh.status_code == 200

    def test_AuthAPIView_201(self):
        username = 'prueba'
        email = 'prueba@test.com'
        password = 'prueba'
        User.objects.create_user(username, email, password)
        path = reverse('tokenObtainPair')
        data = {'user': username, 'pass': password}
        path = reverse('tokenObtainPair')
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        view = AuthAPIView.as_view()
        response = view(request)
        assert response.status_code == 201
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_AuthAPIView_401(self):
        username = 'prueba'
        email = 'prueba@test.com'
        password = 'prueba'
        User.objects.create_user(username, email, password)
        path = reverse('tokenObtainPair')
        data = {'user': username, 'pass': 'prueba2'}
        path = reverse('tokenObtainPair')
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        view = AuthAPIView.as_view()
        response = view(request)
        assert response.status_code == 401
        data = {'user': username, 'pass2': password}
        path = reverse('tokenObtainPair')
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        view = AuthAPIView.as_view()
        response = view(request)
        assert response.status_code == 401
        data = {'user2': username, 'pass': password}
        path = reverse('tokenObtainPair')
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        view = AuthAPIView.as_view()
        response = view(request)
        assert response.status_code == 401
