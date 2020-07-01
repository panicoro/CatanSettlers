import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from catan.models import Board, Game
from catan.views.board_views import BoardInfo, BoardList
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
class TestViewsBoards(TestCase):

    def setUp(self):
        self.board_1 = mixer.blend('catan.Board', name='board_1')
        self.board_2 = mixer.blend('catan.Board', name='board_2')
        self.hexe_1 = mixer.blend('catan.Hexe', terrain='ore', token=8,
                                  level=1, index=4, board=self.board_2)
        self.hexe_2 = mixer.blend('catan.Hexe', terrain='wood', token=8,
                                  level=2, index=10, board=self.board_2)
        self.user = mixer.blend(User, username='Vero', password='roock')
        self.token = AccessToken()

    def test_board_list(self):
        path = reverse('Boards')
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = BoardList.as_view()
        response = view(request)
        assert response.status_code == 200
        assert response.data == [{'id': 1, 'name': 'board_1'},
                                 {'id': 2, 'name': 'board_2'}]

    def test_board_info(self):
        game = mixer.blend('catan.Game', id=1, name='Game_1',
                           board=self.board_2,
                           robber=self.hexe_1)
        path = reverse('BoardInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = BoardInfo.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200
        expected_data = [{'position': {'level': 1, 'index': 4},
                         'terrain': 'ore', 'token': 8},
                         {'position': {'level': 2, 'index': 10},
                         'terrain': 'wood', 'token': 8}]
        assert expected_data == response.data['hexes']
