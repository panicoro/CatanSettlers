from django.test import TestCase, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from catan.models import *
from catan.views.game_views import GameList, GameInfo
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import json


@pytest.mark.django_db
class TestView(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()

    def test_GameList(self):
        robber = mixer.blend('catan.Hexe', level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=robber)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        user2 = mixer.blend(User, username='Pablo', password='minombrepablo')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='yellow',
                              development_cards=1, resources_cards=2)
        player2 = mixer.blend(Player, username=user2,
                              game=game1, colour='green',
                              development_cards=1, resources_cards=2)
        current_turn = mixer.blend(Current_Turn, game=game1, user=user1)
        path = reverse('Games')
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = GameList.as_view()
        response = view(request)
        assert response.status_code == 200
        expected_data = [{'id': 1, 'name': 'Juego', 'in_turn': 'Nico'}]
        assert response.data == expected_data

    def test_GameInfoNoExists(self):
        path = reverse('GameInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = GameInfo.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 404

    def test_GameInfo(self):
        robber = mixer.blend('catan.Hexe', level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=robber)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        user2 = mixer.blend(User, username='Pablo', password='minombrepablo')
        player1 = mixer.blend('catan.Player', username=user1,
                              game=game1, colour='yellow',
                              development_cards=1, resources_cards=2)
        player2 = mixer.blend('catan.Player', username=user2,
                              game=game1, colour='green',
                              development_cards=1, resources_cards=2)
        current_turn = mixer.blend('catan.Current_Turn', game=game1,
                                   user=user1)
        resource1 = mixer.blend('catan.Resource', owner=player1,
                                game=game1, name='wool',
                                last_gained=True)
        building = mixer.blend('catan.Building',
                               name="settlement", owner=player2,
                               level=2, index=6, game=game1)
        road = mixer.blend('catan.Road', owner=player1,
                           game=game1, level_1=1, level_2=1,
                           index_1=2, index_2=1)
        path = reverse('GameInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = GameInfo.as_view()
        response = view(request, pk=1)
        expected_data = {'robber': {'level': 1, 'index': 2},
                         'current_turn': {'user': 'Nico',
                                          'dice': [1, 1]},
                         'winner': None,
                         'players': [{'username': 'Nico',
                                      'colour': 'yellow',
                                      'victory_points': 0,
                                      'resources_cards': 1,
                                      'development_cards': 0,
                                      'roads': [[{'level': 1, 'index': 2},
                                                 {'level': 1, 'index': 1}]],
                                      'last_gained': ['wool'],
                                      'settlements': [],
                                      'cities': []},
                                     {'username': 'Pablo',
                                      'colour': 'green',
                                      'victory_points': 0,
                                      'resources_cards': 0,
                                      'development_cards': 0,
                                      'roads': [], 'last_gained': [],
                                      'settlements': [{'level': 2,
                                                       'index': 6}],
                                      'cities': []}]}
        assert response.data == expected_data
        assert response.status_code == 200
