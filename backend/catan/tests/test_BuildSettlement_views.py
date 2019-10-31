from django.test import TestCase, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from catan.models import *
from catan.views import *
from catan.dices import *
from aux.generateBoard import *
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import json


@pytest.mark.django_db
class TestViews:

    def test_build_vertex1(self):
        self.token = AccessToken()
        vertex_1 = VertexPosition.objects.create(level=1, index=16)
        vertex_2 = VertexPosition.objects.create(level=2, index=26)
        hexe_position = HexePosition.objects.create(level=2, index=11)
        board = Board.objects.create(name='Colonos')
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='catan',
                                           password='catan41')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player1 = Player.objects.create(turn=1, username=request.user,
                                        colour='Red', game=game,
                                        development_cards=1,
                                        resources_cards=4,
                                        victory_points=0)
        road = Road.objects.create(owner=player1, vertex_1=vertex_1,
                                   vertex_2=vertex_2, game=game)
        brick = Resource.objects.create(owner=player1, game=game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=player1, game=game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=player1, game=game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=player1, game=game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 200

    def test_build_vertex2(self):
        self.token = AccessToken()
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        vertex_1 = VertexPosition.objects.create(level=1, index=16)
        vertex_2 = VertexPosition.objects.create(level=2, index=26)
        hexe_position = HexePosition.objects.create(level=2, index=11)
        board = Board.objects.create(name='Colonos')
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='catan',
                                           password='catan41')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player1 = Player.objects.create(turn=1, username=request.user,
                                        colour='Red', game=game,
                                        development_cards=1,
                                        resources_cards=4,
                                        victory_points=0)
        road = Road.objects.create(owner=player1, vertex_1=vertex_1,
                                   vertex_2=vertex_2, game=game)
        brick = Resource.objects.create(owner=player1, game=game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=player1, game=game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=player1, game=game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=player1, game=game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200

    def test_invalidPosition_road(self):
        self.token = AccessToken()
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        vertex_1 = VertexPosition.objects.create(level=1, index=16)
        vertex_2 = VertexPosition.objects.create(level=2, index=26)
        hexe_position = HexePosition.objects.create(level=2, index=11)
        board = Board.objects.create(name='Colonos')
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='catan',
                                           password='catan41')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player1 = Player.objects.create(turn=1, username=request.user,
                                        colour='Red', game=game,
                                        development_cards=1,
                                        resources_cards=4,
                                        victory_points=0)
        brick = Resource.objects.create(owner=player1, game=game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=player1, game=game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=player1, game=game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=player1, game=game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403

    def test_invalidPosition_build(self):
        self.token = AccessToken()
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        vertex_1 = VertexPosition.objects.create(level=1, index=16)
        vertex_2 = VertexPosition.objects.create(level=2, index=26)
        hexe_position = HexePosition.objects.create(level=2, index=11)
        board = Board.objects.create(name='Colonos')
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='catan',
                                           password='catan41')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player1 = Player.objects.create(turn=1, username=request.user,
                                        colour='Red', game=game,
                                        development_cards=1,
                                        resources_cards=4,
                                        victory_points=0)
        road = Road.objects.create(owner=player1, vertex_1=vertex_1,
                                   vertex_2=vertex_2, game=game)
        build = Building.objects.create(game=game, name='city', owner=player1,
                                        position=vertex_1)
        brick = Resource.objects.create(owner=player1, game=game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=player1, game=game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=player1, game=game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=player1, game=game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403

    def test_busyPosition(self):
        self.token = AccessToken()
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        vertex_1 = VertexPosition.objects.create(level=1, index=16)
        vertex_2 = VertexPosition.objects.create(level=2, index=26)
        hexe_position = HexePosition.objects.create(level=2, index=11)
        board = Board.objects.create(name='Colonos')
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='catan',
                                           password='catan41')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player1 = Player.objects.create(turn=1, username=request.user,
                                        colour='Red', game=game,
                                        development_cards=1,
                                        resources_cards=4,
                                        victory_points=0)
        road = Road.objects.create(owner=player1, vertex_1=vertex_1,
                                   vertex_2=vertex_2, game=game)
        build = Building.objects.create(game=game, name='city', owner=player1,
                                        position=vertex_2)
        brick = Resource.objects.create(owner=player1, game=game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=player1, game=game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=player1, game=game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=player1, game=game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403

    def test_noResource(self):
        self.token = AccessToken()
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        vertex_1 = VertexPosition.objects.create(level=1, index=16)
        vertex_2 = VertexPosition.objects.create(level=2, index=26)
        hexe_position = HexePosition.objects.create(level=2, index=11)
        board = Board.objects.create(name='Colonos')
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='catan',
                                           password='catan41')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player1 = Player.objects.create(turn=1, username=request.user,
                                        colour='Red', game=game,
                                        development_cards=1,
                                        resources_cards=4,
                                        victory_points=0)
        road = Road.objects.create(owner=player1, vertex_1=vertex_1,
                                   vertex_2=vertex_2, game=game)
        brick = Resource.objects.create(owner=player1, game=game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=player1, game=game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=player1, game=game,
                                       resource_name="wool")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
