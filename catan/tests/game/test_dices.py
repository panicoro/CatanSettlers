from django.test import TestCase, RequestFactory
from django.urls import reverse
from catan.models import *
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from aux.generateBoard import generateBoardTest, TYPE_RESOURCE
from catan.views.players_views import PlayerInfo
from catan.views.game_views import GameInfo
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import json


@pytest.mark.django_db
class TestView(TestCase):

    def setUp(self):
        self.robber = mixer.blend('catan.Hexe', level=2, index=3)
        self.board = mixer.blend('catan.Board', name='Colonos')
        self.game1 = mixer.blend('catan.Game', name='Juego',
                                 board=self.board,
                                 robber=self.robber)
        self.user1 = mixer.blend(User, username='Nico',
                                 password='minombrenico')
        self.player1 = mixer.blend(Player, username=self.user1,
                                   game=self.game1, colour='red')
        self.turn = Current_Turn.objects.create(game=self.game1,
                                                user=self.user1)
        self.token = AccessToken()

    def test_set_not_last_gained(self):
        resource = mixer.blend('catan.Resource', owner=self.player1,
                               game=self.game1, name='wool',
                               last_gained=True)
        self.player1.set_not_last_gained()
        resource = Resource.objects.filter(id=1, owner=self.player1)[0]
        assert resource.last_gained is False

    def test_gain_resources(self):
        self.player1.gain_resources('wool', 1)
        self.player1.gain_resources('brick', 1)
        self.player1.gain_resources('lumber', 1)
        self.player1.gain_resources('ore', 2)
        self.player1.gain_resources('grain', 2)
        url_game = reverse('GameInfo', kwargs={'pk': 1})
        request_game = RequestFactory().get(url_game)
        force_authenticate(request_game, user=self.user1, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=1)
        url_player = reverse('PlayerInfo', kwargs={'pk': 1})
        request_player = RequestFactory().get(url_player)
        force_authenticate(request_player, user=self.user1, token=self.token)
        view_player = PlayerInfo.as_view()
        response_player = view_player(request_player, pk=1)
        assert len(response_player.data['resources']) == 7
        assert response_player.data['resources'] == ['wool', 'brick',
                                                     'lumber', 'ore', 'ore',
                                                     'grain', 'grain']
        assert response_player.status_code == 200
        assert response_game.data['players'][0]['resources_cards'] == 7
        assert response_game.data['players'][0]['last_gained'] == ['wool',
                                                                   'brick',
                                                                   'lumber',
                                                                   'ore',
                                                                   'ore',
                                                                   'grain',
                                                                   'grain']
        assert response_game.status_code == 200

    def test_throw_dices(self):
        board_test = generateBoardTest()
        game_test = Game.objects.create(name='Juego', board=board_test,
                                        robber=self.robber)
        current_turn = Current_Turn.objects.create(game=game_test,
                                                   user=self.user1)
        player_test = mixer.blend(Player, username=self.user1,
                                  game=game_test, colour='red')
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                level=0, index=0)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                level=1, index=12)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                level=1, index=6)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                level=2, index=4)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                level=2, index=29)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                level=0, index=3)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                level=1, index=3)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                level=1, index=15)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                level=2, index=1)
        throws = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                  (2, 6), (3, 6), (5, 5), (6, 5), (6, 6)]
        expected_resources = TYPE_RESOURCE + TYPE_RESOURCE
        hexes_positions = [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4],
                           [1, 5], [2, 0], [2, 1], [2, 2]]
        for i in range(10):
            hexe = Hexe.objects.get(board=board_test,
                                    level=hexes_positions[i][0],
                                    index=hexes_positions[i][1])
            game_test.robber = hexe
            game_test.save()
            game_test.throw_dices(dice1=throws[i][0], dice2=throws[i][1])
            url_game = reverse('GameInfo', kwargs={'pk': 2})
            request_game = RequestFactory().get(url_game)
            force_authenticate(request_game, user=self.user1, token=self.token)
            view_game = GameInfo.as_view()
            response_game = view_game(request_game, pk=2)
            print(hexe.index)
            print(hexe.level)
            assert response_game.data['players'][0][
                                      'resources_cards'] == 0
            assert response_game.data['players'][0]['last_gained'] == []
        game_test.robber = self.robber
        game_test.save()
        for i in range(10):
            self.player1.set_not_last_gained()
            game_test.throw_dices(dice1=throws[i][0], dice2=throws[i][1])
            url_game = reverse('GameInfo', kwargs={'pk': 2})
            request_game = RequestFactory().get(url_game)
            force_authenticate(request_game, user=self.user1, token=self.token)
            view_game = GameInfo.as_view()
            response_game = view_game(request_game, pk=2)
            assert response_game.data['players'][0][
                                      'resources_cards'] == (i+1)*3
            assert response_game.data['players'][0]['last_gained'] == [
                                       expected_resources[i]] * 3
            assert response_game.status_code == 200

    def test_throw_dices_7(self):
        board_test = generateBoardTest()
        game_test = Game.objects.create(name='Juego', board=board_test,
                                        robber=self.robber)
        current_turn = Current_Turn.objects.create(game=game_test,
                                                   user=self.user1)
        player_test = mixer.blend(Player, username=self.user1,
                                  game=game_test, colour='red')
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                level=0, index=0)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                level=2, index=11)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                level=1, index=2)
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                level=2, index=2)
        game_test.throw_dices(dice1=3, dice2=4)
        url_game = reverse('GameInfo', kwargs={'pk': 2})
        request_game = RequestFactory().get(url_game)
        force_authenticate(request_game, user=self.user1, token=self.token)
        view_game = GameInfo.as_view()
        response_game = view_game(request_game, pk=2)
        assert response_game.data['players'][0][
                                  'resources_cards'] == 0
        assert response_game.data['players'][0]['last_gained'] == []
        assert response_game.status_code == 200
