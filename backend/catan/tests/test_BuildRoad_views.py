import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from catan.models import *
from catan.views import BuildRoad
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
from catan.cargaJson import *


@pytest.mark.django_db
class TestViews:

    def test_build_road_case1_403(self):
        self.token = AccessToken()
        path = reverse('BuildRoad', kwargs={'pk': 1})
        vert_position1 = VertexPosition.objects.create(level=1, index=18)
        vert_position2 = VertexPosition.objects.create(level=2, index=1)
        hexe_position = HexePosition.objects.create(level=0, index=0)
        board = Board.objects.create(name='Colonos')

        data = {"type": "build_road",
                "payload": {"level1": "1", "index1": "18",
                            "level2": "2", "index2": "1"}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='nvero',
                                           password='bariloche')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='Juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player = Player.objects.create(turn=1, username=request.user,
                                       colour='YELLOW', game=game,
                                       development_cards=0, resources_cards=2,
                                       victory_points=0)

        view = BuildRoad.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403

    def test_build_road_case2_403(self):
        self.token = AccessToken()
        path = reverse('BuildRoad', kwargs={'pk': 1})
        vert_position1 = VertexPosition.objects.create(level=1, index=18)
        vert_position2 = VertexPosition.objects.create(level=2, index=1)
        hexe_position = HexePosition.objects.create(level=0, index=0)
        board = Board.objects.create(name='Colonos')

        data = {"type": "build_road",
                "payload": {"level1": "1", "index1": "18",
                            "level2": "2", "index2": "1"}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='nvero',
                                           password='bariloche')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='Juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player = Player.objects.create(turn=1, username=request.user,
                                       colour='YELLOW', game=game,
                                       development_cards=0, resources_cards=2,
                                       victory_points=0)

        Resource.objects.create(owner=player, game=game, resource_name='brick')
        Resource.objects.create(owner=player, game=game,
                                resource_name='lumber')
        view = BuildRoad.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403

    def test_build_road_case3_403(self):
        self.token = AccessToken()
        path = reverse('BuildRoad', kwargs={'pk': 1})
        vert_position1 = VertexPosition.objects.create(level=1, index=18)
        vert_position2 = VertexPosition.objects.create(level=2, index=1)
        hexe_position = HexePosition.objects.create(level=0, index=0)
        board = Board.objects.create(name='Colonos')

        data = {"type": "build_road",
                "payload": {"level1": "1", "index1": "18",
                            "level2": "2", "index2": "1"}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='nvero',
                                           password='bariloche')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='Juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player = Player.objects.create(turn=1, username=request.user,
                                       colour='YELLOW', game=game,
                                       development_cards=0, resources_cards=2,
                                       victory_points=0)

        Resource.objects.create(owner=player, game=game, resource_name='brick')
        Resource.objects.create(owner=player, game=game,
                                resource_name='lumber')
        Road.objects.create(owner=player, vertex_1=vert_position1,
                            vertex_2=vert_position2, game=game)

        view = BuildRoad.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403

    def test_build_road_200(self):
        self.token = AccessToken()
        path = reverse('BuildRoad', kwargs={'pk': 1})
        vert_position1 = VertexPosition.objects.create(level=1, index=18)
        vert_position2 = VertexPosition.objects.create(level=2, index=1)

        vp1 = VertexPosition.objects.create(level=2, index=0)
        vp2 = VertexPosition.objects.create(level=2, index=29)

        hexe_position = HexePosition.objects.create(level=0, index=0)
        board = Board.objects.create(name='Colonos')

        data = {"type": "build_road",
                "payload": {"level1": "1", "index1": "18",
                            "level2": "2", "index2": "1"}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')

        request.user = User.objects.create(username='nvero',
                                           password='bariloche')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='Juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player = Player.objects.create(turn=1, username=request.user,
                                       colour='YELLOW', game=game,
                                       development_cards=0, resources_cards=2,
                                       victory_points=0)

        Resource.objects.create(owner=player, game=game, resource_name='brick')
        Resource.objects.create(owner=player, game=game,
                                resource_name='lumber')

        road = Road.objects.create(owner=player, vertex_1=vp1, vertex_2=vp2,
                                   game=game)
        building = Building.objects.create(game=game, name='settlement',
                                           owner=player,
                                           position=vert_position1)

        view = BuildRoad.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200
