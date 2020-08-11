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
        self.user = mixer.blend(User, username=self.username,
                                email=self.email)
        self.token = AccessToken()
        self.board = mixer.blend('catan.Board', name='Colonos')
        self.hexe = mixer.blend('catan.Hexe', terrain='desert',
                                token=2, board=self.board)
        self.game = mixer.blend('catan.Game', id=1, name='juego1',
                                board=self.board,
                                robber=self.hexe,
                                winner=self.user)
        self.player = mixer.blend('catan.Player', turn=1, username=self.user,
                                  colour='red', game=self.game,
                                  victory_points=0)
        self.turn = mixer.blend('catan.Current_Turn', game=self.game,
                                user=self.user, dices1=3,
                                dices2=3, game_stage='FULL_PLAY')
        self.road = mixer.blend('catan.Road', owner=self.player,
                                level_1=1, level_2=2,
                                index_1=16, index_2=26,
                                game=self.game)
        self.brick = mixer.blend('catan.Resource', owner=self.player,
                                 game=self.game,
                                 name="brick")
        self.lumber = mixer.blend('catan.Resource', owner=self.player,
                                  game=self.game,
                                  name="lumber")
        self.wool = mixer.blend('catan.Resource', owner=self.player,
                                game=self.game,
                                name="wool")
        self.grain = mixer.blend('catan.Resource', owner=self.player,
                                 game=self.game,
                                 name="grain")

    def get_info_game(self, pk):
        path_game = reverse('GameInfo', kwargs={'pk': pk})
        request_game = RequestFactory().get(path_game)
        force_authenticate(request_game, user=self.user, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=pk)
        return response_game

    def get_info_player(self, pk):
        path_player = reverse('PlayerInfo', kwargs={'pk': pk})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=pk)
        return response_player

    def resources_for_city(self):
        mixer.blend('catan.Resource', owner=self.player,
                    game=self.game,
                    name="grain")
        mixer.blend('catan.Resource', owner=self.player,
                    game=self.game,
                    name="ore")
        mixer.blend('catan.Resource', owner=self.player,
                    game=self.game,
                    name="ore")
        mixer.blend('catan.Resource', owner=self.player,
                    game=self.game,
                    name="ore")

    def delete_resources_settl(self):
        self.grain.delete()
        self.lumber.delete()
        self.brick.delete()
        self.wool.delete()

    def test_no_vertex(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 100, "index": 106}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Non-existent position"}
        assert response.status_code == 403

    def test_no_vertex_city(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "upgrade_city",
                "payload": {"level": 100, "index": 106}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Non-existent position"}
        assert response.status_code == 403

    def test_no_turn(self):
        new_user = mixer.blend(User, username='catan', email='matilde13')
        self.turn.user = new_user
        self.turn.save()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Not in turn"}
        assert response.status_code == 403

    def test_no_turn_city(self):
        self.resources_for_city()
        new_user = mixer.blend(User, username='catan', email='matilde13')
        build = mixer.blend('catan.Building', game=self.game,
                            name='settlement',
                            owner=self.player, level=1, index=16)
        self.turn.user = new_user
        self.turn.save()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "upgrade_city",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) == 8
        assert response_game.data['players'][0]['settlements'] == [
            {'level': 1, 'index': 16}
        ]
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Not in turn"}
        assert response.status_code == 403

    def test_build_vertex_1(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert response.status_code == 200
        assert response_player.data['resources'] == []
        assert response_game.data['players'][
               0]['settlements'][0]['level'] == 1
        assert response_game.data['players'][
               0]['settlements'][0]['index'] == 16
        assert response_game.data['players'][0]['victory_points'] == 1

    def test_build_city(self):
        self.resources_for_city()
        build = mixer.blend('catan.Building', game=self.game,
                            name='settlement',
                            owner=self.player, level=1, index=16)
        self.player.gain_points(1)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "upgrade_city",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert response.status_code == 200
        assert response_player.data['resources'] == ['brick', 'lumber', 'wool']
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['cities'] == [
            {'level': 1, 'index': 16}]
        assert response_game.data['players'][0]['victory_points'] == 2

    def test_build_vertex_2(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert response_player.data['resources'] == []
        assert response_game.data['players'][
               0]['settlements'][0]['level'] == 2
        assert response_game.data['players'][
               0]['settlements'][0]['index'] == 26
        assert response_game.data['players'][0]['victory_points'] == 1
        assert response.status_code == 200

    def test_invalid_position_road(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        self.road.delete()
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Invalid position"}
        assert response.status_code == 403

    def test_invalid_position_build(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        build = mixer.blend('catan.Building', game=self.game, name='city',
                            owner=self.player, level=1, index=16)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Invalid position"}
        assert response.status_code == 403

    def test_busy_position(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        build = mixer.blend('catan.Building', game=self.game, name='city',
                            owner=self.player,
                            level=2, index=26)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "Busy position"}
        assert response.status_code == 403

    def test_upgrade_non_existent_build(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "upgrade_city",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail":
                                 "Must upgrade an existent settlement"}
        assert response.status_code == 403

    def test_no_resource_settlement(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        self.grain.delete()
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) < 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail": "It does not have" +
                                 "the necessary resources"}
        assert response.status_code == 403

    def test_no_resource_city(self):
        build = mixer.blend('catan.Building', game=self.game,
                            name='settlement',
                            owner=self.player, level=1, index=16)
        self.player.gain_points(1)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "upgrade_city",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) == 4
        assert response_game.data['players'][0]['settlements'] == [
            {'level': 1, 'index': 16}
        ]
        assert response_game.data['players'][0]['cities'] == []
        assert response_game.data['players'][0]['victory_points'] == 1
        assert response.data == {"detail": "It does not have" +
                                 "the necessary resources"}
        assert response.status_code == 403

    def test_no_time_for_build(self):
        self.turn.game_stage = 'FIRST_CONSTRUCTION'
        self.turn.last_action = 'BUILD_SETTLEMENT'
        self.turn.save()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        self.grain.delete()
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) < 4
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['victory_points'] == 0
        assert response.data == {"detail":
                                 "You cannot construct at this momment"}
        assert response.status_code == 403

    def test_no_time_for_build_city(self):
        self.turn.game_stage = 'FIRST_CONSTRUCTION'
        self.turn.last_action = 'BUILD_SETTLEMENT'
        self.turn.save()
        self.player.gain_points(1)
        build = mixer.blend('catan.Building', game=self.game,
                            name='settlement',
                            owner=self.player, level=1, index=16)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "upgrade_city",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        self.grain.delete()
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert len(response_player.data['resources']) < 4
        assert response_game.data['players'][0]['settlements'] == [
            {'level': 1, 'index': 16}
        ]
        assert response_game.data['players'][0]['victory_points'] == 1
        assert response.data == {"detail":
                                 "You cannot construct at this momment"}
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

    def test_build_gain_free_resources(self):
        self.delete_resources_settl()
        self.turn.game_stage = 'SECOND_CONSTRUCTION'
        self.turn.save()
        mixer.blend('catan.Hexe', board=self.board, level=1, index=4,
                    terrain='ore', token=5)
        mixer.blend('catan.Hexe', board=self.board, level=2, index=8,
                    terrain='brick', token=7)
        mixer.blend('catan.Hexe', board=self.board, level=1, index=3,
                    terrain='grain', token=2)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 1, "index": 12}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert response.status_code == 200
        assert response_player.data['resources'] == ['ore', 'brick', 'grain']
        assert response_game.data['players'][
               0]['settlements'][0]['level'] == 1
        assert response_game.data['players'][
               0]['settlements'][0]['index'] == 12
        assert response_game.data['players'][0]['victory_points'] == 1

    def test_get_with_resources(self):
        mixer.blend('catan.Road', owner=self.player, game=self.game,
                    level_1=1, index_1=17, level_2=2, index_2=29)
        mixer.blend('catan.Road', owner=self.player, game=self.game,
                    level_1=1, index_1=16, level_2=1, index_2=17)
        mixer.blend('catan.Road', owner=self.player, game=self.game,
                    level_1=2, index_1=26, level_2=1, index_2=16)
        mixer.blend('catan.Building', owner=self.player, game=self.game,
                    level=2, index=26)
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
            'type': 'build_road',
            'payload':
                    [
                        [{'level': 2, 'index': 29}, {'level': 2, 'index': 28}],
                        [{'level': 2, 'index': 29}, {'level': 2, 'index': 0}],
                        [{'level': 1, 'index': 16}, {'level': 1, 'index': 15}],
                        [{'level': 1, 'index': 17}, {'level': 1, 'index': 0}],
                        [{'level': 2, 'index': 26}, {'level': 2, 'index': 27}],
                        [{'level': 2, 'index': 26}, {'level': 2, 'index': 25}]
                    ]
        }
        assert response.data[1] == expected_data_roads
        assert expected_data_roads in response.data
        assert response.status_code == 200

    def test_get_with_resources_2(self):
        # In this test we build a new settlement in the position
        # (1, 17) so there isn't a place to build...
        mixer.blend('catan.Road', owner=self.player, game=self.game,
                    level_1=1, index_1=17, level_2=2, index_2=29)
        mixer.blend('catan.Road', owner=self.player, game=self.game,
                    level_1=1, index_1=16, level_2=1, index_2=17)
        mixer.blend('catan.Road', owner=self.player, game=self.game,
                    level_1=2, index_1=26, level_2=1, index_2=16)
        mixer.blend('catan.Building', owner=self.player, game=self.game,
                    level=2, index=26, name='settlement')
        mixer.blend('catan.Building', owner=self.player, game=self.game,
                    level=1, index=17, name='settlement')
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = {
            'type': 'build_road',
            'payload':
                [
                    [{'level': 2, 'index': 29}, {'level': 2, 'index': 28}],
                    [{'level': 2, 'index': 29}, {'level': 2, 'index': 0}],
                    [{'level': 1, 'index': 16}, {'level': 1, 'index': 15}],
                    [{'level': 1, 'index': 17}, {'level': 1, 'index': 0}],
                    [{'level': 2, 'index': 26}, {'level': 2, 'index': 27}],
                    [{'level': 2, 'index': 26}, {'level': 2, 'index': 25}]
                ]
        }
        assert expected_data == response.data[1]
        assert response.status_code == 200

    def test_winner_settlement(self):
        self.player.gain_points(9)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert response_player.data['resources'] == []
        assert response_game.data['players'][
               0]['settlements'][0]['level'] == 2
        assert response_game.data['players'][
               0]['settlements'][0]['index'] == 26
        assert response_game.data['winner'] == 'test_user'
        assert response_game.data['players'][0]['victory_points'] == 10
        assert response.data == {'detail': 'YOU WIN!!!'}
        assert response.status_code == 200

    def test_winner_city(self):
        self.resources_for_city()
        build = mixer.blend('catan.Building', game=self.game,
                            name='settlement',
                            owner=self.player, level=2, index=26)
        self.player.gain_points(9)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "upgrade_city",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        response_game = self.get_info_game(1)
        response_player = self.get_info_player(1)
        assert response_player.data['resources'] == ['brick', 'lumber', 'wool']
        assert response_game.data['players'][0]['settlements'] == []
        assert response_game.data['players'][0]['cities'] == [
            {"level": 2, "index": 26}
        ]
        assert response_game.data['winner'] == 'test_user'
        assert response_game.data['players'][0]['victory_points'] == 10
        assert response.data == {'detail': 'YOU WIN!!!'}
        assert response.status_code == 200

    def test_get_initial_settlements(self):
        self.delete_resources_settl()
        self.road.delete()
        self.turn.game_stage = 'FIRST_CONSTRUCTION'
        self.turn.last_action = 'NON_BLOCKING_ACTION'
        self.turn.save()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = {
            'payload': [{'index': 0, 'level': 0}, {'index': 1, 'level': 0},
                        {'index': 2, 'level': 0}, {'index': 3, 'level': 0},
                        {'index': 4, 'level': 0}, {'index': 5, 'level': 0},
                        {'index': 0, 'level': 1}, {'index': 1, 'level': 1},
                        {'index': 2, 'level': 1}, {'index': 3, 'level': 1},
                        {'index': 4, 'level': 1}, {'index': 5, 'level': 1},
                        {'index': 6, 'level': 1}, {'index': 7, 'level': 1},
                        {'index': 8, 'level': 1}, {'index': 9, 'level': 1},
                        {'index': 10, 'level': 1}, {'index': 11, 'level': 1},
                        {'index': 12, 'level': 1}, {'index': 13, 'level': 1},
                        {'index': 14, 'level': 1}, {'index': 15, 'level': 1},
                        {'index': 16, 'level': 1}, {'index': 17, 'level': 1},
                        {'index': 0, 'level': 2},  {'index': 1, 'level': 2},
                        {'index': 2, 'level': 2},  {'index': 3, 'level': 2},
                        {'index': 4, 'level': 2},  {'index': 5, 'level': 2},
                        {'index': 6, 'level': 2},  {'index': 7, 'level': 2},
                        {'index': 8, 'level': 2},  {'index': 9, 'level': 2},
                        {'index': 10, 'level': 2}, {'index': 11, 'level': 2},
                        {'index': 12, 'level': 2}, {'index': 13, 'level': 2},
                        {'index': 14, 'level': 2}, {'index': 15, 'level': 2},
                        {'index': 16, 'level': 2}, {'index': 17, 'level': 2},
                        {'index': 18, 'level': 2}, {'index': 19, 'level': 2},
                        {'index': 20, 'level': 2}, {'index': 21, 'level': 2},
                        {'index': 22, 'level': 2}, {'index': 23, 'level': 2},
                        {'index': 24, 'level': 2}, {'index': 25, 'level': 2},
                        {'index': 26, 'level': 2}, {'index': 27, 'level': 2},
                        {'index': 28, 'level': 2}, {'index': 29, 'level': 2}],
            'type': 'build_settlement'
        }
        assert expected_data == response.data[0]
        assert response.status_code == 200

    def test_get_initial_settlements_2(self):
        self.delete_resources_settl()
        mixer.blend('catan.Building', name='settlement', level=1, index=16,
                    owner=self.player, game=self.game)
        self.turn.game_stage = 'SECOND_CONSTRUCTION'
        self.turn.last_action = 'NON_BLOCKING_ACTION'
        self.turn.save()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = {
            'payload': [{'index': 0, 'level': 0}, {'index': 1, 'level': 0},
                        {'index': 2, 'level': 0}, {'index': 3, 'level': 0},
                        {'index': 4, 'level': 0}, {'index': 5, 'level': 0},
                        {'index': 0, 'level': 1}, {'index': 1, 'level': 1},
                        {'index': 2, 'level': 1}, {'index': 3, 'level': 1},
                        {'index': 4, 'level': 1}, {'index': 5, 'level': 1},
                        {'index': 6, 'level': 1}, {'index': 7, 'level': 1},
                        {'index': 8, 'level': 1}, {'index': 9, 'level': 1},
                        {'index': 10, 'level': 1}, {'index': 11, 'level': 1},
                        {'index': 12, 'level': 1}, {'index': 13, 'level': 1},
                        {'index': 14, 'level': 1}, {'index': 0, 'level': 2},
                        {'index': 1, 'level': 2}, {'index': 2, 'level': 2},
                        {'index': 3, 'level': 2}, {'index': 4, 'level': 2},
                        {'index': 5, 'level': 2}, {'index': 6, 'level': 2},
                        {'index': 7, 'level': 2}, {'index': 8, 'level': 2},
                        {'index': 9, 'level': 2}, {'index': 10, 'level': 2},
                        {'index': 11, 'level': 2}, {'index': 12, 'level': 2},
                        {'index': 13, 'level': 2}, {'index': 14, 'level': 2},
                        {'index': 15, 'level': 2}, {'index': 16, 'level': 2},
                        {'index': 17, 'level': 2}, {'index': 18, 'level': 2},
                        {'index': 19, 'level': 2}, {'index': 20, 'level': 2},
                        {'index': 21, 'level': 2}, {'index': 22, 'level': 2},
                        {'index': 23, 'level': 2}, {'index': 24, 'level': 2},
                        {'index': 25, 'level': 2}, {'index': 27, 'level': 2},
                        {'index': 28, 'level': 2}, {'index': 29, 'level': 2}],
            'type': 'build_settlement'
        }
        assert expected_data == response.data[0]
        assert response.status_code == 200

    def test_get_cities_no_settl(self):
        self.resources_for_city()
        self.delete_resources_settl()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == [{'type': 'end_turn'}]
        assert response.status_code == 200

    def test_get_cities_no_resources(self):
        mixer.blend('catan.Building', name='settlement', level=1, index=16,
                    owner=self.player, game=self.game)
        self.road.delete()
        self.brick.delete()
        self.lumber.delete()
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == [{'type': 'end_turn'}]
        assert response.status_code == 200

    def test_get_cities(self):
        self.resources_for_city()
        mixer.blend('catan.Building', name='settlement', level=1, index=16,
                    owner=self.player, game=self.game)
        mixer.blend('catan.Building', name='settlement', level=0, index=3,
                    owner=self.player, game=self.game)
        mixer.blend('catan.Building', name='city', level=1, index=8,
                    owner=self.player, game=self.game)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert {'payload': [{'index': 16, 'level': 1},
                            {'index': 3, 'level': 0}],
                'type': 'upgrade_city'
                } in response.data
        assert response.status_code == 200
