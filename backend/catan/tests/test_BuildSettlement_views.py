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
class TestViews(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()
        self.vertex_1 = VertexPosition.objects.create(level=1, index=16)
        self.vertex_2 = VertexPosition.objects.create(level=2, index=26)
        self.hexe_position = HexePosition.objects.create(level=2, index=11)
        self.board = Board.objects.create(name='Colonos')
        self.game = Game.objects.create(id=1, name='juego1', board=self.board,
                                        robber=self.hexe_position,
                                        winner=self.user)
        self.player = Player.objects.create(turn=1, username=self.user,
                                            colour='Red', game=self.game,
                                            development_cards=1,
                                            resources_cards=4,
                                            victory_points=0)

    def test_build_vertex1(self):
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 1, "index": 16}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        road = Road.objects.create(owner=self.player, vertex_1=self.vertex_1,
                                   vertex_2=self.vertex_2, game=self.game)
        brick = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=self.player, game=self.game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=self.player, game=self.game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 200

    def test_build_vertex2(self):
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        road = Road.objects.create(owner=self.player, vertex_1=self.vertex_1,
                                   vertex_2=self.vertex_2, game=self.game)
        brick = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=self.player, game=self.game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=self.player, game=self.game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200

    def test_invalidPosition_road(self):
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        brick = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=self.player, game=self.game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=self.player, game=self.game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403

    def test_invalidPosition_build(self):
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        road = Road.objects.create(owner=self.player, vertex_1=self.vertex_1,
                                   vertex_2=self.vertex_2, game=self.game)
        build = Building.objects.create(game=self.game, name='city',
                                        owner=self.player,
                                        position=self.vertex_1)
        brick = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=self.player, game=self.game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=self.player, game=self.game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403

    def test_busyPosition(self):
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        build = Building.objects.create(game=self.game, name='city',
                                        owner=self.player,
                                        position=self.vertex_2)
        road = Road.objects.create(owner=self.player, vertex_1=self.vertex_1,
                                   vertex_2=self.vertex_2, game=self.game)
        brick = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=self.player, game=self.game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=self.player, game=self.game,
                                       resource_name="wool")
        grain = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="grain")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403

    def test_noResource(self):
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        data = {"type": "build_settlement",
                "payload": {"level": 2, "index": 26}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        road = Road.objects.create(owner=self.player, vertex_1=self.vertex_1,
                                   vertex_2=self.vertex_2, game=self.game)
        brick = Resource.objects.create(owner=self.player, game=self.game,
                                        resource_name="brick")
        lumber = Resource.objects.create(owner=self.player, game=self.game,
                                         resource_name="lumber")
        wool = Resource.objects.create(owner=self.player, game=self.game,
                                       resource_name="wool")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
