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
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = mixer.blend(User, username=self.username, email=self.email)
        self.token = AccessToken()
        self.board = mixer.blend('catan.Board', name='Colonos')
        self.hexe = mixer.blend('catan.Hexe', level=2, index=11,
                                terrain='desert',
                                token=2, board=self.board)
        self.game = mixer.blend('catan.Game', id=1, name='juego1',
                                board=self.board,
                                robber=self.hexe)
        self.player = mixer.blend('catan.Player', turn=1, username=self.user,
                                  colour='RED', game=self.game,
                                  victory_points=0)
        self.turn = mixer.blend('catan.Current_Turn', game=self.game,
                                user=self.user,
                                dices1=3,
                                dices2=3)
        self.ore = mixer.blend('catan.Resource', owner=self.player,
                               game=self.game,
                               name="ore")
        self.wool = mixer.blend('catan.Resource', owner=self.player,
                                game=self.game,
                                name="wool")
        self.grain = mixer.blend('catan.Resource', owner=self.player,
                                 game=self.game,
                                 name="grain")

    def get_game_info(self, pk):
        path_game = reverse('GameInfo', kwargs={'pk': pk})
        request_game = RequestFactory().get(path_game)
        force_authenticate(request_game, user=self.user, token=self.token)
        view_game = GameInfo.as_view()
        return view_game(request_game, pk=pk)

    def get_player_info(self, pk):
        path_player = reverse('PlayerInfo', kwargs={'pk': pk})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        return view_player(request_player, pk=pk)

    def test_buy_card(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "buy_card"}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
        assert response_player.data['resources'] == []
        card = response_player.data['cards'][0]
        assert card in ['knight', 'victory_point', 'year_of_plenty',
                        'road_building', 'monopoly']
        assert response_game.data['players'][0]['development_cards'] == 1
        assert response.status_code == 200

    def test_no_resource(self):
        self.grain.delete()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "buy_card"}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
        assert response_player.data['resources'] != []
        assert response_player.data['cards'] == []
        assert response_game.data['players'][0]['development_cards'] == 0
        assert response.data == {"detail": "It does not have" +
                                 " the necessary resources"}
        assert response.status_code == 403

    def test_buy_card_winner(self):
        self.player.victory_points = 9
        self.player.save()
        Card.objects.create(owner=self.player,
                            game=self.game, name='victory_point')
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "buy_card"}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200
        assert response.data == {'detail': 'YOU WIN!!!'}

    def test_get_bank_trade(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert {"type": 'buy_card'} in response.data
        assert response.status_code == 200
