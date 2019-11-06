import pytest
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from catan.models import *
from aux.generateBoard import *
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
        generateVertexPositions()
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()
        self.vert_position1 = VertexPosition.objects.get(level=2, index=0)
        self.vert_position2 = VertexPosition.objects.get(level=2, index=1)
        self.vp2 = VertexPosition.objects.get(level=2, index=2)
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

    def test_not_turn(self):
        user = User.objects.create_user(username='nvero', email='bariloche')
        self.turn.user = user
        self.turn.save()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 1},
                            {"level": 2, "index": 2}]}
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
        assert len(response_player.data['resources']) == 2
        assert len(response_game.data['players'][0]['roads']) == 1
        assert response.data == {"detail": "Not in turn"}
        assert response.status_code == 403

    def test_not_neighbor(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        vert_position1 = VertexPosition.objects.get(level=2, index=18)
        vert_position2 = VertexPosition.objects.get(level=2, index=20)
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 18},
                            {"level": 2, "index": 20}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == {'detail': 'not neighbor'}
        assert response.status_code == 403

    def test_invalid_position(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 0},
                            {"level": 2, "index": 1}]}
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
        assert len(response_player.data['resources']) == 2
        assert len(response_game.data['players'][0]['roads']) == 1
        assert response.data == {'detail': 'invalid position, reserved'}
        assert response.status_code == 403

    def test_build_road(self):
        self.token = AccessToken()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 1},
                            {"level": 2, "index": 2}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='nvero',
                                           password='bariloche')
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
        assert len(response_player.data['resources']) == 0
        assert response_game.data['players'][0]['resources_cards'] == 0
        assert response_game.data['players'][0]['roads'][0][0]['level'] == 2
        assert response_game.data['players'][0]['roads'][0][0]['index'] == 0
        assert response_game.data['players'][0]['roads'][0][1]['level'] == 2
        assert response_game.data['players'][0]['roads'][0][1]['index'] == 1
        assert response_game.data['players'][0]['roads'][1][0]['level'] == 2
        assert response_game.data['players'][0]['roads'][1][0]['index'] == 1
        assert response_game.data['players'][0]['roads'][1][1]['level'] == 2
        assert response_game.data['players'][0]['roads'][1][1]['index'] == 2
        assert len(response_game.data['players'][0]['roads']) == 2
        assert response.status_code == 200

    def test_nothing_built(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 1},
                            {"level": 2, "index": 2}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        self.road.delete()
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
        assert len(response_player.data['resources']) == 2
        assert response_game.data['players'][0]['roads'] == []
        assert response.data == {'detail': 'must have something built'}
        assert response.status_code == 403
        assert response_game.data['players'][0]['resources_cards'] == 2

    def test_not_resource(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 1},
                            {"level": 2, "index": 2}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        self.brick.delete()
        self.lumber.delete()
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
        assert len(response_player.data['resources']) == 0
        assert len(response_game.data['players'][0]['roads']) == 1
        assert response.data == {'detail': "Doesn't have enough resources"}
        assert response.status_code == 403

    def test_not_vertex_position(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 200, "index": 10000},
                            {"level": 2, "index": 2}]}
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
        assert len(response_player.data['resources']) == 2
        assert len(response_game.data['players'][0]['roads']) == 1
        assert response.data == {"detail": "Non-existent vetertexs positions"}
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

    def test_get_withResource1(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = [{
            'type': 'build_road',
            'payload': [[{'level': 2, 'index': 0},
                         {'level': 2, 'index': 29}],
                        [{'level': 2, 'index': 1},
                         {'level': 1, 'index': 1}],
                        [{'level': 2, 'index': 1},
                         {'level': 2, 'index': 2}]],
            }
        ]
        assert response.data == expected_data
        assert response.status_code == 200

    def test_get_withResource2(self):
        """
        This test delete the one road and then create a building in
        the board
        """
        self.road.delete()
        Building.objects.create(owner=self.player, game=self.game,
                                position=self.vert_position2)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = [{
            'type': 'build_road',
            'payload': [[{'level': 2, 'index': 1},
                         {'level': 2, 'index': 0}],
                        [{'level': 2, 'index': 1},
                         {'level': 1, 'index': 1}],
                        [{'level': 2, 'index': 1},
                         {'level': 2, 'index': 2}]],
            }
        ]
        assert response.data == expected_data
        assert response.status_code == 200

    def test_get_withResource3(self):
        """
        This test only create a building in the board
        """
        Building.objects.create(owner=self.player, game=self.game,
                                position=self.vert_position2)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = [{
            'type': 'build_road',
            'payload': [[{'level': 2, 'index': 0},
                         {'level': 2, 'index': 29}],
                        [{'level': 2, 'index': 1},
                         {'level': 1, 'index': 1}],
                        [{'level': 2, 'index': 1},
                         {'level': 2, 'index': 2}]],
            }
        ]
        assert response.data == expected_data
        assert response.status_code == 200

    def test_get_withResource4(self):
        """
        This test delete the only road existent
        """
        self.road.delete()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == []
        assert response.status_code == 200
