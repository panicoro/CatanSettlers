from django.test import RequestFactory
#from catan.views import BuildRoad
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
from catan.cargaJson import *
from django.test import TestCase
from catan.models import *
from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
class TestView(TestCase):
    def test_VertexInfo(self):
        vert_pos = VertexPosition.objects.create(level=1, index=16)
        aux_vec = [[2, 26], [1, 17], [1, 15]]

        self.assertEqual(VertexInfo(vert_pos.level, vert_pos.index), aux_vec)

    def test_CheckRoads_Road(self):
        hexe_position = HexePosition.objects.create(level=0, index=0)

        vert_position1 = VertexPosition.objects.create(level=1, index=18)
        vert_position2 = VertexPosition.objects.create(level=2, index=1)

        vp1 = VertexPosition.objects.create(level=2, index=18)
        vp2 = VertexPosition.objects.create(level=2, index=20)

        user = User.objects.create(username='nvero', password='bariloche')
        board = Board.objects.create(name='Colonos')
        game = Game.objects.create(id=1, name='Juego1', board=board,
                                   robber=hexe_position, winner=user)
        player = Player.objects.create(turn=1, username=user,
                                       colour='YELLOW', game=game,
                                       development_cards=0,
                                       resources_cards=2,
                                       victory_points=0)

        Road.objects.create(owner=player, vertex_1=vert_position1,
                            vertex_2=vert_position2, game=game)
        Road.objects.create(owner=player, vertex_1=vp1, vertex_2=vp2,
                            game=game)

        list_road = Road.objects.filter(owner=player, game=game)

        self.assertTrue(CheckRoads_Road(list_road, vert_position1.level,
                                        vert_position1.index, 2, 21))
        self.assertTrue(CheckRoads_Road(list_road, 2, 21, vert_position2.level,
                                        vert_position2.index))
        self.assertTrue(CheckRoads_Road(list_road, 2, 21, vert_position2.level,
                                        18))
        self.assertTrue(CheckRoads_Road(list_road, 2, 1, vert_position1.level,
                                        0))

    def test_CheckBuild_Road(self):
        hexe_position = HexePosition.objects.create(level=0, index=0)

        vert_position1 = VertexPosition.objects.create(level=1, index=18)
        vert_position2 = VertexPosition.objects.create(level=2, index=1)

        user = User.objects.create(username='nvero', password='bariloche')
        board = Board.objects.create(name='Colonos')

        game = Game.objects.create(id=1, name='Juego1', board=board,
                                   robber=hexe_position, winner=user)
        player = Player.objects.create(turn=1, username=user,
                                       colour='YELLOW', game=game,
                                       development_cards=0, resources_cards=2,
                                       victory_points=0)

        Building.objects.create(game=game, name='settlement', owner=player,
                                position=vert_position1)
        Building.objects.create(game=game, name='settlement', owner=player,
                                position=vert_position2)

        list_build = Building.objects.filter(owner=player, game=game)

        self.assertEqual(CheckBuild_Road(list_build, vert_position1.level,
                                         vert_position1.index,
                                         2, 21), True)
        self.assertEqual(CheckBuild_Road(list_build, 2, 21,
                                         vert_position2.level,
                                         vert_position2.index), True)

    def test_CheckPositionRoad(self):
        hexe_position = HexePosition.objects.create(level=0, index=0)

        vert_position1 = VertexPosition.objects.create(level=1, index=18)
        vert_position2 = VertexPosition.objects.create(level=2, index=1)

        vp1 = VertexPosition.objects.create(level=0, index=6)
        vp2 = VertexPosition.objects.create(level=0, index=5)

        user = User.objects.create(username='nvero', password='bariloche')
        board = Board.objects.create(name='Colonos')

        game = Game.objects.create(id=1, name='Juego1', board=board,
                                   robber=hexe_position, winner=user)

        player = Player.objects.create(turn=1, username=user,
                                       colour='RED', game=game,
                                       development_cards=0, resources_cards=4,
                                       victory_points=0)

        Road.objects.create(owner=player, vertex_1=vert_position1,
                            vertex_2=vert_position2, game=game)
        Road.objects.create(owner=player, vertex_1=vp1,
                            vertex_2=vp2, game=game)

        list_road = Road.objects.filter(owner=player, game=game)

        self.assertTrue(CheckPositionRoad(list_road, vert_position1.level,
                        vert_position1.index, vert_position2.level,
                        vert_position2.index))
        self.assertTrue(CheckPositionRoad(list_road, vert_position2.level,
                        vert_position2.index, vert_position1.level,
                        vert_position1.index))
        self.assertFalse(CheckPositionRoad(list_road, 0, 1, 0, 2))
        self.assertFalse(CheckPositionRoad(list_road, 2, 14, 2, 13))

    def test_deleteResource(self):
        hexe_position = HexePosition.objects.create(level=0, index=0)
        vert_position1 = VertexPosition.objects.create(level=1, index=18)
        vert_position2 = VertexPosition.objects.create(level=2, index=1)

        user = User.objects.create(username='nvero', password='bariloche')
        board = Board.objects.create(name='Colonos')

        game = Game.objects.create(id=1, name='Juego1', board=board,
                                   robber=hexe_position, winner=user)

        player = Player.objects.create(turn=1, username=user,
                                       colour='RED', game=game,
                                       development_cards=0, resources_cards=2,
                                       victory_points=0)

        Resource.objects.create(owner=player, game=game, resource_name='brick')
        Resource.objects.create(owner=player, game=game,
                                resource_name='lumber')
        list_resource = Resource.objects.filter(owner=player, game=game)

        Road.objects.create(owner=player, vertex_1=vert_position1,
                                   vertex_2=vert_position2, game=game)

        self.assertEqual(deleteResource(list_resource), None)
