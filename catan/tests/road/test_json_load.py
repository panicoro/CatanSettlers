from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
from catan.views.actions.road import *
from django.test import TestCase
from catan.models import *
from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
class TestView(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = mixer.blend(User, username=self.username, email=self.email)
        self.token = AccessToken()
        self.board = mixer.blend('catan.Board', name='Colonos')
        self.hexe = mixer.blend('catan.Hexe', terrain=0, level=0, index=0,
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
        self.building_1 = mixer.blend('catan.Building', game=self.game,
                                      name='settlement', owner=self.player,
                                      index=2,  level=0)
        self.building_1 = mixer.blend('catan.Building', game=self.game,
                                      name='settlement', owner=self.player,
                                      index=2,  level=1)

    def test_is_neighbor(self):
        self.assertEqual(are_neighbors(2, 18, 2, 20), False)
        self.assertEqual(are_neighbors(2, 0, 2, 1), True)

    def test_vertex_info(self):
        aux_vec = [[2, 26], [1, 17], [1, 15]]
        self.assertEqual(VertexInfo(1, 16), aux_vec)
