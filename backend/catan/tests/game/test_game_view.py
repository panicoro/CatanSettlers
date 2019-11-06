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
        hexe_position = HexePosition.objects.create(level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
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

    def test_GameInfoNoExists(self):
        path = reverse('GameInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = GameInfo.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 404

    def test_GameInfo(self):
        hexe_position = HexePosition.objects.create(level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        user2 = mixer.blend(User, username='Pablo', password='minombrepablo')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='yellow',
                              development_cards=1, resources_cards=2)
        player2 = mixer.blend(Player, username=user2,
                              game=game1, colour='green',
                              development_cards=1, resources_cards=2)
        current_turn = mixer.blend(Current_Turn, game=game1, user=user1)
        vertex1 = VertexPosition.objects.create(level=1, index=2)
        vertex2 = VertexPosition.objects.create(level=1, index=1)
        resource1 = mixer.blend(Resource, owner=player1,
                                game=game1, resource_name='wool',
                                last_gained=True)
        road = mixer.blend(Road, owner=player1,
                           game=game1, vertex_1=vertex1, vertex_2=vertex2)
        path = reverse('GameInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = GameInfo.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 200
