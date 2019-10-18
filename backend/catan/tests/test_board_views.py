import pytest
from django.test import RequestFactory
from catan.views import BoardInfo
from django.urls import reverse
from rest_framework import status
from catan.models import Game, Board, Hexes


@pytest.mark.django_db
class TestViews:
    def test_BoardInfo(self):
        path = reverse('BoardInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.board = Board.objects.create(name = 'Colonos')
        view = BoardInfo.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200