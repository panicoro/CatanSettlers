import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from catan.views.login_views import Register
from django.urls import reverse


@pytest.mark.django_db
class TestViews:
    def test_Register_views(self):
        username = 'prueba'
        password = 'prueba'
        path = reverse('register')
        data = {'user': username, 'pass': password}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        view = Register.as_view()
        response = view(request)
        assert response.status_code == 200
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        response = view(request)
        assert response.status_code == 409
        data = {}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        view = Register.as_view()
        response = view(request)
        assert response.status_code == 400
