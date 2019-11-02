from django.test import RequestFactory
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

    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()
        self.hexe_position = HexePosition.objects.create(level=0, index=0)
        self.vert_pos1 = VertexPosition.objects.create(level=2, index=0)
        self.vert_pos2 = VertexPosition.objects.create(level=2, index=1)
        self.board = Board.objects.create(name='Colonos')
        self.game = Game.objects.create(id=1, name='Juego1', board=self.board,
                                        robber=self.hexe_position,
                                        winner=self.user)
        self.player = Player.objects.create(turn=1, username=self.user,
                                            colour='YELLOW', game=self.game,
                                            development_cards=0,
                                            resources_cards=2,
                                            victory_points=0)
        self.brick = Resource.objects.create(owner=self.player, game=self.game,
                                             resource_name='brick')
        self.lumber = Resource.objects.create(owner=self.player,
                                              game=self.game,
                                              resource_name='lumber')
        self.road = Road.objects.create(owner=self.player,
                                        vertex_1=self.vert_pos1,
                                        vertex_2=self.vert_pos2,
                                        game=self.game)
        self.building1 = Building.objects.create(game=self.game,
                                                 name='settlement',
                                                 owner=self.player,
                                                 position=self.vert_pos1)
        self.building2 = Building.objects.create(game=self.game,
                                                 name='settlement',
                                                 owner=self.player,
                                                 position=self.vert_pos2)

    def test_is_neighbor(self):
        vp1 = VertexPosition.objects.create(level=2, index=18)
        vp2 = VertexPosition.objects.create(level=2, index=20)
        list_vec = VertexInfo(vp1.level, vp1.index)
        self.assertEqual(is_neighbor(list_vec, vp2.level, vp2.index), False)
        list_neighbor = VertexInfo(self.vert_pos1.level, self.vert_pos1.index)
        self.assertEqual(is_neighbor(list_neighbor, self.vert_pos2.level,
                                     self.vert_pos2.index), True)

    def test_VertexInfo(self):
        vert_pos = VertexPosition.objects.create(level=1, index=16)
        aux_vec = [[2, 26], [1, 17], [1, 15]]

        self.assertEqual(VertexInfo(vert_pos.level, vert_pos.index), aux_vec)

    def test_CheckRoads_Road(self):
        list_vec = VertexInfo(self.vert_pos1.level, self.vert_pos1.index)
        self.assertEqual(is_neighbor(list_vec, self.vert_pos2.level,
                                     self.vert_pos2.index), True)
        assert CheckRoads_Road(self.player.id, self.game.id,
                               self.vert_pos1.level,
                               self.vert_pos1.index, 2, 29) is True
        assert CheckRoads_Road(self.player.id, self.game.id,
                               self.vert_pos2.level,
                               self.vert_pos2.index, 1, 1) is True
        assert CheckRoads_Road(self.player.id, self.game.id, 1, 1,
                               self.vert_pos2.level,
                               self.vert_pos2.index) is True
        assert CheckRoads_Road(self.player.id, self.game.id, 1, 1,
                               self.vert_pos1.level,
                               self.vert_pos1.index) is True
        assert CheckRoads_Road(self.player.id, self.game.id, 1, 17, 1,
                               16) is False

    def test_CheckBuild_Road(self):
        assert CheckBuild_Road(self.player.id, self.game.id,
                               self.vert_pos1.level,
                               self.vert_pos1.index, 1, 1) is True
        assert CheckBuild_Road(self.player.id, self.game.id, 1, 1,
                               self.vert_pos2.level,
                               self.vert_pos2.index) is True
        assert CheckBuild_Road(self.player.id, self.game.id, 1, 17, 1,
                               16) is False

    def test_CheckPositionRoad(self):
        assert CheckPositionRoad(self.game.id, self.vert_pos1.level,
                                 self.vert_pos1.index, self.vert_pos2.level,
                                 self.vert_pos2.index) is True
        assert CheckPositionRoad(self.game.id, self.vert_pos2.level,
                                 self.vert_pos2.index, self.vert_pos1.level,
                                 self.vert_pos1.index) is True
        assert CheckPositionRoad(self.game.id, self.vert_pos1.level,
                                 self.vert_pos1.index, 1, 1) is False

    def test_deleteResource(self):
        assert deleteResource(self.player.id, self.game.id) is None
