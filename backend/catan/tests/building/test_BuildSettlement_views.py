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
        generateVertexPositions()
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()
        self.vertex_1 = VertexPosition.objects.get(level=1, index=16)
        self.vertex_2 = VertexPosition.objects.get(level=2, index=26)
        self.hexe_position = HexePosition.objects.create(level=2, index=11)
        self.board = Board.objects.create(name='Colonos')
        self.game = Game.objects.create(id=1, name='juego1', board=self.board,
                                        robber=self.hexe_position,
                                        winner=self.user)
        self.player = Player.objects.create(turn=1, username=self.user,
                                            colour='red', game=self.game,
                                            victory_points=0)
        self.turn = Current_Turn.objects.create(game=self.game,
                                                user=self.user,
                                                dices1=3,
                                                dices2=3)
        self.road = Road.objects.create(owner=self.player,
                                        vertex_1=self.vertex_1,
                                        vertex_2=self.vertex_2,
                                        game=self.game)
        self.brick = Resource.objects.create(owner=self.player,
                                             game=self.game,
                                             resource_name="brick")
        self.lumber = Resource.objects.create(owner=self.player,
                                              game=self.game,
                                              resource_name="lumber")
        self.wool = Resource.objects.create(owner=self.player,
                                            game=self.game,
                                            resource_name="wool")
        self.grain = Resource.objects.create(owner=self.player,
                                             game=self.game,
                                             resource_name="grain")

    def test_noVertex(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 100, "index": 106}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response.render()
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
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Non-existent position"}
        assert response.status_code == 403

    def test_noTurn(self):
        user = User.objects.create_user(username='catan', email='matilde13')
        self.turn.user = user
        self.turn.save()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response.render()
        path_game = reverse('GameInfo', kwargs={'pk': 1})
        request_game = RequestFactory().get(path)
        force_authenticate(request_game, user=self.user, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=1)
        path_player = reverse('PlayerInfo', kwargs={'pk': 1})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Not in turn"}
        assert response.status_code == 403

    def test_build_vertex1(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response.render()
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
        assert response_game.data['players'][
               0]['settlements'][0]['level'] == 1
        assert response_game.data['players'][
               0]['settlements'][0]['index'] == 16
        assert response_game.data['players'][0]['victory_points'] == 1
        assert response.status_code == 200

    def test_build_vertex2(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
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
        assert response_game.data['players'][
               0]['settlements'][0]['level'] == 2
        assert response_game.data['players'][
               0]['settlements'][0]['index'] == 26
        assert response_game.data['players'][0]['victory_points'] == 1
        assert response.status_code == 200

    def test_invalidPosition_road(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        self.road.delete()
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        path_game = reverse('GameInfo', kwargs={'pk': 1})
        request_game = RequestFactory().get(path)
        force_authenticate(request_game, user=self.user, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=1)
        path_player = reverse('PlayerInfo', kwargs={'pk': 1})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Invalid position"}
        assert response.status_code == 403

    def test_invalidPosition_build(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        build = Building.objects.create(game=self.game, name='city',
                                        owner=self.player,
                                        position=self.vertex_1)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        path_game = reverse('GameInfo', kwargs={'pk': 1})
        request_game = RequestFactory().get(path)
        force_authenticate(request_game, user=self.user, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=1)
        path_player = reverse('PlayerInfo', kwargs={'pk': 1})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Invalid position"}
        assert response.status_code == 403

    def test_busyPosition(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        build = Building.objects.create(game=self.game, name='city',
                                        owner=self.player,
                                        position=self.vertex_2)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        path_game = reverse('GameInfo', kwargs={'pk': 1})
        request_game = RequestFactory().get(path)
        force_authenticate(request_game, user=self.user, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=1)
        path_player = reverse('PlayerInfo', kwargs={'pk': 1})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Busy position"}
        assert response.status_code == 403

    def test_noResource(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        self.grain.delete()
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        path_game = reverse('GameInfo', kwargs={'pk': 1})
        request_game = RequestFactory().get(path)
        force_authenticate(request_game, user=self.user, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=1)
        path_player = reverse('PlayerInfo', kwargs={'pk': 1})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=1)
        assert len(response_player.data['resources']) < 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "It does not have" +
                                 "the necessary resources"}
        assert response.status_code == 403

    def test_get_noResource(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        self.lumber.delete()
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == []
        assert response.status_code == 200

    def test_get_withResources(self):
        new_vertex1 = VertexPosition.objects.get(level=1, index=17)
        new_vertex2 = VertexPosition.objects.get(level=2, index=29)
        Road.objects.create(owner=self.player, game=self.game,
                            vertex_1=new_vertex1, vertex_2=new_vertex2)
        Road.objects.create(owner=self.player, game=self.game,
                            vertex_1=self.vertex_1, vertex_2=new_vertex1)
        Road.objects.create(owner=self.player, game=self.game,
                            vertex_1=self.vertex_2, vertex_2=self.vertex_1)
        Building.objects.create(owner=self.player, game=self.game,
                                position=self.vertex_2)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data_buildings = { 
            "type": "build_settlement",
            "payload": [{"level": 1, "index": 17},
                         {"level": 2, "index": 29}]}
        expected_data_roads = {
            "type": "build_road",
            "payload": [
                 [{'level': 2, 'index': 26}, {'level': 2, 'index': 27}],
                 [{'level': 2, 'index': 26}, {'level': 2, 'index': 25}],
                 [{'level': 2, 'index': 29}, {'level': 2, 'index': 28}],
                 [{'level': 2, 'index': 29}, {'level': 2, 'index': 0}],
                 [{'level': 1, 'index': 16}, {'level': 1, 'index': 15}],
                 [{'level': 1, 'index': 17}, {'level': 1, 'index': 0}]]}
        assert expected_data_buildings in response.data
        assert expected_data_roads in response.data
        assert response.status_code == 200

    def test_get_withResources2(self):
        """
        In this test we build a new settlement in the position
        (1, 17) so there isn't a place to build...
        """
        new_vertex1 = VertexPosition.objects.get(level=1, index=17)
        new_vertex2 = VertexPosition.objects.get(level=2, index=29)
        Road.objects.create(owner=self.player, game=self.game,
                            vertex_1=new_vertex1, vertex_2=new_vertex2)
        Road.objects.create(owner=self.player, game=self.game,
                            vertex_1=self.vertex_1, vertex_2=new_vertex1)
        Road.objects.create(owner=self.player, game=self.game,
                            vertex_1=self.vertex_2, vertex_2=self.vertex_1)
        Building.objects.create(owner=self.player, game=self.game,
                                position=self.vertex_2)
        Building.objects.create(owner=self.player, game=self.game,
                                position=new_vertex1)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = [
            {"type": "build_road",
             "payload": [
                 [{'level': 2, 'index': 26}, {'level': 2, 'index': 27}],
                 [{'level': 2, 'index': 26}, {'level': 2, 'index': 25}],
                 [{'level': 2, 'index': 29}, {'level': 2, 'index': 28}],
                 [{'level': 2, 'index': 29}, {'level': 2, 'index': 0}],
                 [{'level': 1, 'index': 16}, {'level': 1, 'index': 15}],
                 [{'level': 1, 'index': 17}, {'level': 1, 'index': 0}]]}
        ]
        assert response.data == expected_data
        assert response.status_code == 200
