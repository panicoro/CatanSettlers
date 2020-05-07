import pytest
from mixer.backend.django import mixer
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


@pytest.mark.django_db
class TestViews(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()
        self.hexe = mixer.blend('catan.Hexe', level=0, index=0)
        self.board = mixer.blend('catan.Board', name='Colonos')
        self.game = mixer.blend('catan.Game', id=1, name='Juego1',
                                board=self.board,
                                robber=self.hexe,
                                winner=self.user)
        self.player = mixer.blend('catan.Player', turn=1, username=self.user,
                                  colour='YELLOW', game=self.game,
                                  victory_points=0)
        self.turn = mixer.blend('catan.Current_Turn', game=self.game,
                                user=self.user,
                                dices1=3, dices2=3,
                                game_stage='FULL_PLAY')
        self.road = mixer.blend('catan.Road', owner=self.player,
                                level_1=2, index_1=0,
                                level_2=2, index_2=1,
                                game=self.game)
        self.cardRoad = mixer.blend('catan.Card', owner=self.player,
                                    game=self.game,
                                    name='road_building')

    def get_info_player(self, pk):
        path_player = reverse('PlayerInfo', kwargs={'pk': pk})
        request_player = RequestFactory().get(path_player)
        force_authenticate(request_player, user=self.user, token=self.token)
        view_player = PlayerInfo.as_view()
        return view_player(request_player, pk=pk)

    def test_road_building_card(self):
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
        assert len(response_game.data['players'][0]['roads']) == 3
        expected_data = [
            [{'level': 2, 'index': 0},
             {'level': 2, 'index': 1}],
            [{'level': 2, 'index': 1},
             {'level': 2, 'index': 2}],
            [{'level': 2, 'index': 2},
             {'level': 2, 'index': 3}]
        ]
        assert response_game.data['players'][0]['roads'] == expected_data
        assert response_game.data['players'][0]['development_cards'] == 0
        assert response.status_code == 200

    def test_road_building_card_one_road(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "play_road_building_card",
                "payload": [[{"level": 2, "index": 1},
                            {"level": 2, "index": 2}],
                            [{"level": 2, "index": 2},
                            {"level": 2, "index": 1000}]]}
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
        assert len(response_game.data['players'][0]['roads']) == 1
        expected_data = [
            [{'level': 2, 'index': 0},
             {'level': 2, 'index': 1}]
        ]
        assert response_game.data['players'][0]['roads'] == expected_data
        assert response_game.data['players'][0]['development_cards'] == 1
        assert response.data == {'detail': 'Non-existent vertexs positions'}
        assert response.status_code == 403

    def test_no_card(self):
        self.cardRoad.delete()
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
        response_player = self.get_info_player(1)
        assert response_player.data['cards'] == []
        expected_data = [
            [{'level': 2, 'index': 0},
             {'level': 2, 'index': 1}]
        ]
        assert response_game.data['players'][0]['roads'] == expected_data
        assert response_game.data['players'][0]['development_cards'] == 0
        assert response.data == {'detail': 'Missing Road Building card'}
        assert response.status_code == 403

    def test_no_vertex(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "play_road_building_card",
                "payload": [[{"level": 200, "index": 1},
                            {"level": 2, "index": 2}],
                            [{"level": 2, "index": 2000},
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
        response_player = self.get_info_player(1)
        assert response_player.data['cards'] == ['road_building']
        expected_data = [
            [{'level': 2, 'index': 0},
             {'level': 2, 'index': 1}]
        ]
        assert response_game.data['players'][0]['roads'] == expected_data
        assert response_game.data['players'][0]['development_cards'] == 1
        assert response.data == {'detail': 'Non-existent vertexs positions'}
        assert response.status_code == 403

    def test_busy_position(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "play_road_building_card",
                "payload": [[{"level": 2, "index": 0},
                            {"level": 2, "index": 1}],
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
        response_player = self.get_info_player(1)
        assert response_player.data['cards'] == ['road_building']
        assert response_game.data['players'][0]['development_cards'] == 1
        expected_data = [
            [{'level': 2, 'index': 0},
             {'level': 2, 'index': 1}]
        ]
        assert response_game.data['players'][0]['roads'] == expected_data
        assert response.data == {'detail': 'Busy position, reserved'}
        assert response.status_code == 403

    def test_no_road(self):
        self.road.delete()
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
        response_player = self.get_info_player(1)
        assert response_player.data['cards'] == ['road_building']
        assert response_game.data['players'][0]['development_cards'] == 1
        assert response_game.data['players'][0]['roads'] == []
        assert response.data == {'detail': 'You must have something built'}
        assert response.status_code == 403

    def test_no_neighbor(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        data = {"type": "play_road_building_card",
                "payload": [[{"level": 2, "index": 5},
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
        response_player = self.get_info_player(1)
        assert response_player.data['cards'] == ['road_building']
        assert response_game.data['players'][0]['development_cards'] == 1
        expected_data = [
            [{'level': 2, 'index': 0},
             {'level': 2, 'index': 1}]
        ]
        assert response_game.data['players'][0]['roads'] == expected_data
        assert response.data == {'detail': 'not neighbors'}
        assert response.status_code == 403

    def test_get_no_card(self):
        url = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(url)
        force_authenticate(request, user=self.user, token=self.token)
        self.cardRoad.delete()
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == [{'type': 'end_turn'}]
        assert response.status_code == 200

    def test_get_with_card_1(self):
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

    def test_get_with_card_2(self):
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = {
            'type': 'play_road_building_card',
            'payload': [[{'level': 2, 'index': 0}, {'level': 2, 'index': 29}],
                        [{'level': 2, 'index': 1}, {'level': 1, 'index': 1}],
                        [{'level': 2, 'index': 1}, {'level': 2, 'index': 2}],
                        [{'level': 2, 'index': 29}, {'level': 2, 'index': 28}],
                        [{'level': 2, 'index': 29}, {'level': 1, 'index': 17}],
                        [{'level': 1, 'index': 1}, {'level': 1, 'index': 0}],
                        [{'level': 1, 'index': 1}, {'level': 1, 'index': 2}],
                        [{'level': 2, 'index': 2}, {'level': 2, 'index': 3}]]
        }
        assert expected_data in response.data
        assert {'type': 'end_turn'} in response.data
        assert response.status_code == 200
