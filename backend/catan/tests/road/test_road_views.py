import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.test import TestCase, RequestFactory
from catan.models import *
from aux.generateBoard import *
from catan.views.players_views import PlayerActions, PlayerInfo
from catan.views.game_views import GameInfo
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
class TestViews(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = mixer.blend(User, username=self.username, email=self.email)
        self.token = AccessToken()
        self.board = mixer.blend('catan.Board', name='Colonos')
        self.hexe = mixer.blend('catan.Hexe', terrain=0,
                                token=2, board=self.board)
        self.game = mixer.blend('catan.Game', id=1, name='Juego1',
                                board=self.board,
                                robber=self.hexe)
        self.player = mixer.blend('catan.Player', turn=1,
                                  username=self.user,
                                  colour='YELLOW', game=self.game,
                                  victory_points=0)
        self.turn = mixer.blend('catan.Current_Turn', game=self.game,
                                user=self.user, dices1=3, dices2=3,
                                game_stage='FULL_PLAY')
        self.brick = mixer.blend('catan.Resource', owner=self.player,
                                 game=self.game, name="brick")
        self.lumber = mixer.blend('catan.Resource', owner=self.player,
                                  game=self.game, name="lumber")
        self.road = mixer.blend('catan.Road', owner=self.player,
                                level_1=2, index_1=0,
                                level_2=2, index_2=1,
                                game=self.game)

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
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
        assert len(response_player.data['resources']) == 2
        assert len(response_game.data['players'][0]['roads']) == 1
        assert response.data == {"detail": "Not in turn"}
        assert response.status_code == 403

    def test_not_neighbor(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 18},
                            {"level": 2, "index": 20}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == {'detail': 'not neighbors'}
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
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
        assert len(response_player.data['resources']) == 2
        assert len(response_game.data['players'][0]['roads']) == 1
        assert response.data == {'detail': 'Busy position, reserved'}
        assert response.status_code == 403

    def test_build_road(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 1},
                            {"level": 2, "index": 2}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
        assert response.status_code == 200
        assert response_player.data['resources'] == []
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

    def test_build_road_first_stage(self):
        self.turn.game_stage = 'FIRST_CONSTRUCTION'
        self.turn.last_action = 'BUILD_SETTLEMENT'
        self.turn.save()
        self.road.delete()
        mixer.blend('catan.Building', owner=self.player,
                    game=self.game, name='settlement',
                    level=2, index=1)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 1},
                            {"level": 2, "index": 2}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
        assert response.status_code == 200
        assert response_player.data['resources'] == ['brick', 'lumber']
        assert response_game.data['players'][0]['resources_cards'] == 2
        assert response_game.data['players'][0]['roads'][0][0]['level'] == 2
        assert response_game.data['players'][0]['roads'][0][0]['index'] == 1
        assert response_game.data['players'][0]['roads'][0][1]['level'] == 2
        assert response_game.data['players'][0]['roads'][0][1]['index'] == 2
        assert len(response_game.data['players'][0]['roads']) == 1

    def test_build_road_first_stage_not_from_last(self):
        self.turn.game_stage = 'FIRST_CONSTRUCTION'
        self.turn.last_action = 'BUILD_SETTLEMENT'
        self.turn.save()
        self.road.delete()
        mixer.blend('catan.Building', owner=self.player,
                    game=self.game, name='settlement',
                    level=2, index=1)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 1, "index": 0},
                            {"level": 1, "index": 1}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
        assert response.status_code == 403
        assert response.data == {"detail":
                                 "You must build since your last building"}
        assert response_player.data['resources'] == ['brick', 'lumber']
        assert response_game.data['players'][0]['resources_cards'] == 2
        assert len(response_game.data['players'][0]['roads']) == 0

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
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
        assert len(response_player.data['resources']) == 2
        assert response_game.data['players'][0]['roads'] == []
        assert response.data == {'detail': 'You must have something built'}
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
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
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
        response_game = self.get_game_info(1)
        response_player = self.get_player_info(1)
        assert len(response_player.data['resources']) == 2
        assert len(response_game.data['players'][0]['roads']) == 1
        assert response.data == {"detail": "Non-existent vertexs positions"}
        assert response.status_code == 403

    def test_get_no_resource(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        self.lumber.delete()
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == [{'type': 'end_turn'}]
        assert response.status_code == 200

    def test_get_with_resource_1(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = {
            'type': 'build_road',
            'payload': [[{'level': 2, 'index': 0},
                         {'level': 2, 'index': 29}],
                        [{'level': 2, 'index': 1},
                         {'level': 1, 'index': 1}],
                        [{'level': 2, 'index': 1},
                         {'level': 2, 'index': 2}]],
        }
        assert expected_data in response.data
        assert response.status_code == 200

    def test_get_with_resource_2(self):
        # This test delete the one road and then create a building in
        # the board
        self.road.delete()
        mixer.blend('catan.Building', owner=self.player, game=self.game,
                    level=2, index=1)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = {
            'type': 'build_road',
            'payload': [[{'level': 2, 'index': 1},
                         {'level': 2, 'index': 0}],
                        [{'level': 2, 'index': 1},
                         {'level': 1, 'index': 1}],
                        [{'level': 2, 'index': 1},
                         {'level': 2, 'index': 2}]],
        }
        assert expected_data in response.data
        assert response.status_code == 200

    def test_get_withResource3(self):
        """
        This test only create a building in the board
        """
        mixer.blend('catan.Building', owner=self.player, game=self.game,
                    level=2, index=1)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = {
            'type': 'build_road',
            'payload': [[{'level': 2, 'index': 0},
                         {'level': 2, 'index': 29}],
                        [{'level': 2, 'index': 1},
                         {'level': 1, 'index': 1}],
                        [{'level': 2, 'index': 1},
                         {'level': 2, 'index': 2}]],
        }
        assert expected_data in response.data
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
        assert response.data == [{'type': 'end_turn'}]
        assert response.status_code == 200
