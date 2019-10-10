import pytest
from django.test import RequestFactory
from catan.views import CardsList
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestViews:
    def test_CardsList(self):
        path = reverse('CardsList', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.create(username = 'Nico', password = 'minombrenico')
        response = CardsList(request, pk=1)
        assert response.status_code == 200
