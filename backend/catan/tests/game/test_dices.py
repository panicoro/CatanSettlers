from django.test import TestCase, RequestFactory
from django.urls import reverse
from catan.models import *
from catan.dices import *
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from aux.generateBoard import *
from catan.views import *
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import json


@pytest.mark.django_db
class TestView(TestCase):

    def setUp(self):
        generateHexesPositions()
        generateVertexPositions()
        self.robber = robber = HexePosition.objects.all()[10]
        self.board = Board.objects.create(name='Colonos')
        self.game1 = Game.objects.create(name='Juego', board=self.board,
                                         robber=self.robber)
        self.user1 = mixer.blend(User, username='Nico',
                                 password='minombrenico')
        self.player1 = mixer.blend(Player, username=self.user1,
                                   game=self.game1, colour='red')
        self.turn = Current_Turn.objects.create(game=self.game1,
                                                user=self.user1)
        self.token = AccessToken()

    def test_set_not_last_gained(self):
        resource = mixer.blend(Resource, owner=self.player1,
                               game=self.game1, resource_name='wool',
                               last_gained=True)
        set_not_last_gained(self.player1)
        resource = Resource.objects.filter(id=1, owner=self.player1)[0]
        assert resource.last_gained is False

    def test_gain_resources(self):
        gain_resources(self.game1, self.player1, 'wool', 1)
        gain_resources(self.game1, self.player1, 'brick', 1)
        gain_resources(self.game1, self.player1, 'lumber', 1)
        gain_resources(self.game1, self.player1, 'ore', 2)
        gain_resources(self.game1, self.player1, 'grain', 2)
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

    def test_throw_dicesSettlements(self):
        board_test = generateBoardTest()
        vertex_positions = VertexPosition.objects.all()
        game_test = Game.objects.create(name='Juego', board=board_test,
                                        robber=self.robber)
        current_turn = Current_Turn.objects.create(game=game_test,
                                                   user=self.user1)
        player_test = mixer.blend(Player, username=self.user1,
                                  game=game_test, colour='red')
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                position=vertex_positions[0])
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                position=vertex_positions[18])
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                position=vertex_positions[12])
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                position=vertex_positions[28])
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='city',
                                position=vertex_positions[53])
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                position=vertex_positions[3])
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                position=vertex_positions[9])
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                position=vertex_positions[21])
        Building.objects.create(game=game_test,
                                owner=player_test,
                                name='settlement',
                                position=vertex_positions[25])
        throws = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                  (2, 6), (3, 6), (5, 5), (6, 5), (6, 6)]
        expected_resources = TYPE_RESOURCE + TYPE_RESOURCE
        hexes_positions = HexePosition.objects.all()[:10]
        for i in range(10):
            game_test.robber = hexes_positions[i]
            game_test.save()
            throw_dices(game_test, dice1=throws[i][0], dice2=throws[i][1])
            url_game = reverse('GameInfo', kwargs={'pk': 2})
            request_game = RequestFactory().get(url_game)
            force_authenticate(request_game, user=self.user1, token=self.token)
            view_game = GameInfo.as_view()
            response_game = view_game(request_game, pk=2)
            assert response_game.data['players'][0][
                                      'resources_cards'] == 0
            assert response_game.data['players'][0]['last_gained'] == []
        game_test.robber = self.robber
        game_test.save()
        for i in range(10):
            set_not_last_gained(self.player1)
            throw_dices(game_test, dice1=throws[i][0], dice2=throws[i][1])
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
