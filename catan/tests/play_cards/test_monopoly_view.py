from django.test import TestCase, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from catan.models import *
from catan.views.players_views import PlayerActions, PlayerInfo
from catan.views.game_views import GameInfo
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import json


@pytest.mark.django_db
class TestViews(TestCase):

    def setUp(self):
        self.user1 = mixer.blend(User, username='user1', password='1234')
        self.token = AccessToken()

    def createGame(self):
        self.user2 = mixer.blend(User, username='user2', password='1234')
        self.user3 = mixer.blend(User, username='user3', password='1234')
        self.user4 = mixer.blend(User, username='user4', password='1234')
        self.board = mixer.blend('catan.Board', name='Board1')
        self.room = mixer.blend('catan.Room', name='Room1', owner=self.user1,
                                board_id=1)
        self.hexe = mixer.blend('catan.Hexe', terrain='ore', token=2,
                                board=self.board, level=1, index=0)
        self.game = mixer.blend('catan.Game', name='Game1', board=self.board,
                                robber=self.hexe)
        self.player1 = mixer.blend(Player, username=self.user1,
                                   game=self.game, colour='yellow')
        self.player2 = mixer.blend(Player, username=self.user2,
                                   game=self.game, colour='green')
        self.player3 = mixer.blend(Player, username=self.user3,
                                   game=self.game, colour='blue')
        self.player4 = mixer.blend(Player, username=self.user4,
                                   game=self.game, colour='red')

    def get_player_info(self, pk, user):
        path_player = reverse('PlayerInfo', kwargs={'pk': pk})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=user, token=self.token)
        view_player = PlayerInfo.as_view()
        return view_player(request_player, pk=pk)

    def test_play_monopoly(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=1)
        Resource.objects.create(
            owner=self.player3, game=self.game, name='ore')
        Resource.objects.create(
            owner=self.player3, game=self.game, name='brick')
        Resource.objects.create(
            owner=self.player3, game=self.game, name='brick')
        Resource.objects.create(
            owner=self.player2, game=self.game, name='brick')
        Resource.objects.create(
            owner=self.player4, game=self.game, name='lumber')
        Resource.objects.create(
            owner=self.player4, game=self.game, name='wool')
        card = Card.objects.create(owner=self.player1,
                                   game=self.game,
                                   name='monopoly')
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "play_monopoly_card",
                "payload": "brick"}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_player = self.get_player_info(1, self.user1)
        assert response_player.data['resources'] == ['brick', 'brick', 'brick']
        response_player = self.get_player_info(1, self.user2)
        assert response_player.data['resources'] == []
        response_player = self.get_player_info(1, self.user3)
        assert response_player.data['resources'] == ['ore']
        response_player = self.get_player_info(1, self.user4)
        assert response_player.data['resources'] == ['lumber', 'wool']
        assert response.status_code == 200

    def test_no_card(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=1)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "play_monopoly_card",
                "payload": "brick"}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == {"detail": 'You have not monopoly card'}
        assert response.status_code == 403

    def test_non_existent_resource(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=1)
        card = Card.objects.create(owner=self.player1,
                                   game=self.game,
                                   name='monopoly')
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "play_monopoly_card",
                "payload": "bribnbnck"}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == {"detail": "Non-existent resource"}
        assert response.status_code == 403

    def test_get_monopoly(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=1)
        card = Card.objects.create(owner=self.player1,
                                   game=self.game,
                                   name='monopoly')
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert {"type": 'play_monopoly_card'} in response.data
        assert response.status_code == 200

    def test_get_monopoly_not_card(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=1)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert [{"type": 'end_turn'}] == response.data
        assert response.status_code == 200
