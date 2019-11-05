from django.test import TestCase, RequestFactory
from catan.models import *
from catan.dices import *
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from aux.generateBoard import *
import pytest
import json


@pytest.mark.django_db
class TestView(TestCase):

    def test_set_not_last_gained(self):
        hexe_position = HexePosition.objects.create(level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        resource = mixer.blend(Resource, owner=player1,
                               game=game1, resource_name='wool',
                               last_gained=True)
        set_not_last_gained(player1)
        resource = Resource.objects.filter(id=1, owner=player1)[0]
        assert resource.last_gained is False

    def test_gain_resources(self):
        hexe_position = HexePosition.objects.create(level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='Rojo')
        gain_resources(game1, player1, 'wool', 3)
        resources = Resource.objects.filter(owner=player1)
        assert len(resources) == 3

    def test_throw_dicesSettlements(self):
        generateHexesPositions()
        hexe_position = HexePosition.objects.all()[0]
        board = generateBoardTest()
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='red')
        current_turn = Current_Turn.objects.create(game=game1, user=user1)
        generateVertexPositions()
        vertex_positions = VertexPosition.objects.all()
        for i in range(0, len(vertex_positions)):
            Building.objects.create(game=game1,
                                    owner=player1,
                                    name='settlement',
                                    position=vertex_positions[i])
        throw_dices(game1, current_turn, board)
        assert len(Resource.objects.filter(owner=player1)) != 0

    def test_throw_dicesCities(self):
        generateHexesPositions()
        hexe_position = HexePosition.objects.all()[0]
        board = generateBoardTest()
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='red')
        current_turn = Current_Turn.objects.create(game=game1, user=user1)
        generateVertexPositions()
        vertex_positions = VertexPosition.objects.all()
        for i in range(0, len(vertex_positions)):
            Building.objects.create(game=game1,
                                    owner=player1,
                                    name='city',
                                    position=vertex_positions[i])
        throw_dices(game1, current_turn, board)
        assert len(Resource.objects.filter(owner=player1)) != 0
