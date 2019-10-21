import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from catan.models import Board, Game, HexePosition
from catan.views import BoardInfo, BoardList, GameList
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestViews:

    def test_GameList(self):
        path = reverse('Games')
        request = RequestFactory().get(path)
        view = GameList.as_view()
        response = view(request)
        assert response.status_code == 200

    def test_BoardList(self):
        path = reverse('Boards')
        request = RequestFactory().get(path)
        request.board = Board.objects.create(name='Colonos')
        view = BoardList.as_view()
        response = view(request)
        assert response.status_code == 200

    def test_BoardInfo(self):
        path = reverse('BoardInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.board = Board.objects.create(name='Colonos')
        hexe_position = HexePosition.objects.create(level=1, index=1)
        user = User.objects.create(username='Vero', password='roock')
        game = Game.objects.create(id=1, name='Juego 1', board=request.board,
                                   roober=hexe_position, winner=user)
        view = BoardInfo.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200
