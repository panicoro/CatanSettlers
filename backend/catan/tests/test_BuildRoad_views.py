import pytest
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from catan.models import *
from catan.views import BuildRoad
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
from catan.cargaJson import *


@pytest.mark.django_db
class TestViews(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()
        self.vert_position1 = VertexPosition.objects.create(level=2, index=0)
        self.vert_position2 = VertexPosition.objects.create(level=2, index=1)
        self.hexe_position = HexePosition.objects.create(level=0, index=0)
        self.board = Board.objects.create(name='Colonos')
        self.game = Game.objects.create(id=1, name='Juego1', board=self.board,
                                        robber=self.hexe_position,
                                        winner=self.user)
        self.player = Player.objects.create(turn=1, username=self.user,
                                            colour='YELLOW', game=self.game,
                                            development_cards=0,
                                            resources_cards=2,
                                            victory_points=0)

    def test_not_neighbor(self):
        path = reverse('BuildRoad', kwargs={'pk': 1})
        vert_position1 = VertexPosition.objects.create(level=2, index=18)
        vert_position2 = VertexPosition.objects.create(level=2, index=20)
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 18},
                            {"level": 2, "index": 20}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = BuildRoad.as_view()
        response = view(request, pk=1)
        assert response.data == {'detail': 'not neighbor'}
        assert response.status_code == 403

    def test_not_resource(self):
        path = reverse('BuildRoad', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 0},
                            {"level": 2, "index": 1}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = BuildRoad.as_view()
        response = view(request, pk=1)
        assert response.data == {'detail': "Doesn't have enough resources"}
        assert response.status_code == 403

    def test_nothing_built(self):
        path = reverse('BuildRoad', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 0},
                            {"level": 2, "index": 1}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        Resource.objects.create(owner=self.player, game=self.game,
                                resource_name='brick')
        Resource.objects.create(owner=self.player, game=self.game,
                                resource_name='lumber')
        view = BuildRoad.as_view()
        response = view(request, pk=1)
        assert response.data == {'detail': 'must have something built'}
        assert response.status_code == 403

    def test_invalid_position(self):
        path = reverse('BuildRoad', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 0},
                            {"level": 2, "index": 1}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        Resource.objects.create(owner=self.player, game=self.game,
                                resource_name='brick')
        Resource.objects.create(owner=self.player, game=self.game,
                                resource_name='lumber')
        Road.objects.create(owner=self.player, vertex_1=self.vert_position1,
                            vertex_2=self.vert_position2, game=self.game)
        view = BuildRoad.as_view()
        response = view(request, pk=1)
        assert response.data == {'detail': 'invalid position, reserved'}
        assert response.status_code == 403

    def test_build_road(self):
        self.token = AccessToken()
        path = reverse('BuildRoad', kwargs={'pk': 1})
        data = {"type": "build_road",
                "payload": [{"level": 2, "index": 0},
                            {"level": 2, "index": 1}]}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='nvero',
                                           password='bariloche')
        force_authenticate(request, user=self.user, token=self.token)
        Resource.objects.create(owner=self.player, game=self.game,
                                resource_name='brick')
        Resource.objects.create(owner=self.player, game=self.game,
                                resource_name='lumber')
        vp2 = VertexPosition.objects.create(level=2, index=2)
        road = Road.objects.create(owner=self.player,
                                   vertex_1=self.vert_position2,
                                   vertex_2=vp2,
                                   game=self.game)
        building = Building.objects.create(game=self.game, name='settlement',
                                           owner=self.player,
                                           position=self.vert_position1)
        view = BuildRoad.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200
