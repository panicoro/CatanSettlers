from django.test import TestCase, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from catan.models import *
from catan.views.players_views import PlayerActions, PlayerInfo
from catan.views.game_views import GameInfo
from catan.dices import *
from aux.generateBoard import *
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import json


@pytest.mark.django_db
class TestViews(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()
        self.hexe_position = HexePosition.objects.create(level=2, index=11)
        self.board = Board.objects.create(name='Colonos')
        self.game = Game.objects.create(id=1, name='juego1', board=self.board,
                                        robber=self.hexe_position,
                                        winner=self.user)
        self.player = Player.objects.create(turn=1, username=self.user,
                                            colour='Red', game=self.game,
                                            victory_points=0)
        self.turn = Current_Turn.objects.create(game=self.game,
                                                user=self.user,
                                                dices1=3,
                                                dices2=3)
        self.ore = Resource.objects.create(owner=self.player,
                                           game=self.game,
                                           resource_name="ore")
        self.wool = Resource.objects.create(owner=self.player,
                                            game=self.game,
                                            resource_name="wool")
        self.grain = Resource.objects.create(owner=self.player,
                                             game=self.game,
                                             resource_name="grain")

    def test_BuyCard(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "buy_card"}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        path_game = reverse('GameInfo', kwargs={'pk': 1})
        request_game = RequestFactory().get(path_game)
        force_authenticate(request_game, user=self.user, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=1)
        path_player = reverse('PlayerInfo', kwargs={'pk': 1})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=1)
        assert response_player.data['resources'] == []
        assert len(response_player.data['cards']) == 1
        assert response_game.data['players'][0]['development_cards'] == 1
        assert response.status_code == 200

    def test_NoResource(self):
        self.grain.delete()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "buy_card"}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        path_game = reverse('GameInfo', kwargs={'pk': 1})
        request_game = RequestFactory().get(path_game)
        force_authenticate(request_game, user=self.user, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=1)
        path_player = reverse('PlayerInfo', kwargs={'pk': 1})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=1)
        assert response_player.data['resources'] != []
        assert response_player.data['cards'] == []
        assert response_game.data['players'][0]['development_cards'] == 0
        assert response.data == {"detail": "It does not have" +
                                 " the necessary resources"}
        assert response.status_code == 403

    def test_BuyCardWinner(self):
        self.player.victory_points = 9
        self.player.save()
        Card.objects.create(owner=self.player,
                            game=self.game, card_name='victory_point')
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "buy_card"}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200
