import pytest
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from catan.models import *
from catan.views.players_views import PlayerActions, PlayerInfo
from catan.views.game_views import GameInfo
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
from catan.cargaJson import *


@pytest.mark.django_db
class TestViews(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()
        self.vert_position1 = VertexPosition.objects.create(level=2, index=0)
        self.vert_position2 = VertexPosition.objects.create(level=2, index=1)
        self.vert_position3 = VertexPosition.objects.create(level=2, index=2)
        self.vert_position4 = VertexPosition.objects.create(level=2, index=3)
        self.hexe_position = HexePosition.objects.create(level=0, index=0)
        self.board = Board.objects.create(name='Colonos')
        self.game = Game.objects.create(id=1, name='Juego1', board=self.board,
                                        robber=self.hexe_position,
                                        winner=self.user)
        self.player = Player.objects.create(turn=1, username=self.user,
                                            colour='YELLOW', game=self.game,
                                            victory_points=0)
        self.turn = Current_Turn.objects.create(game=self.game,
                                                user=self.user,
                                                dices1=3,
                                                dices2=3)
        self.brick = Resource.objects.create(owner=self.player,
                                             game=self.game,
                                             resource_name="brick")
        self.lumber = Resource.objects.create(owner=self.player,
                                              game=self.game,
                                              resource_name="lumber")
        self.road = Road.objects.create(owner=self.player,
                                        vertex_1=self.vert_position1,
                                        vertex_2=self.vert_position2,
                                        game=self.game)
        self.cardRoad = Card.objects.create(owner=self.player, game=self.game, card_name='road_building')


    def test_roadBuilding_card(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "play_road_building_card",
                "payload": [[{"level": 2, "index": 1},
                            {"level": 2, "index": 2}],
                            [{"level": 2, "index": 2},
                            {"level": 2, "index": 3}]]}
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
        response_game.render()
        print(response_game.data['players'][0]['roads'])
        path_player = reverse('PlayerInfo', kwargs={'pk': 1})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=1)
        print(response_player.data['resources'])
        assert len(response_player.data['resources']) == 2
        assert len(response_game.data['players'][0]['roads'][0]) == 2
        print(response.data)
        assert response.status_code == 200
