import pytest
from django.test import RequestFactory
from catan.views import PlayerInfo
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestViews:
    def test_PlayerInfo(self):
        path = reverse('PlayerInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User, username='Nico',
                                   password='minombrenico')
        view = PlayerInfo.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200
