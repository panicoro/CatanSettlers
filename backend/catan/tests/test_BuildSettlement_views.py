import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from catan.models import *
from catan.views import BuildSettlement
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
class TestViews:

    def test_build_settlement(self):
        self.token = AccessToken()
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        vert_position = VertexPosition.objects.create(level=1, index=16)
        hexe_position = HexePosition.objects.create(level=2, index=11)
        board = Board.objects.create(name='Colonos')
        data = {"type": "build_settlement",
                "payload": {"level": "1", "index": "16"}}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        request.user = User.objects.create(username='fedemarkco',
                                           password='fedemarkco')
        force_authenticate(request, user=request.user, token=self.token)
        game = Game.objects.create(id=1, name='juego1', board=board,
                                   robber=hexe_position, winner=request.user)
        player1 = Player.objects.create(turn=1, username=request.user,
                                        colour='Red', game=game,
                                        development_cards=1, resources_cards=4,
                                        victory_points=0)
        for i in range(4):
            Resource.objects.create(owner=player1, game=game,
                                    resource_name="brick")
        view = BuildSettlement.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200
