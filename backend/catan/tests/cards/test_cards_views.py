import pytest
from django.test import RequestFactory
from catan.views import PlayerInfo
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from catan.models import *
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
class TestViews:
    def test_PlayerInfo(self):
        self.token = AccessToken()
        path = reverse('PlayerInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User, username='Nico',
                                   password='minombrenico')
        force_authenticate(request, user=request.user, token=self.token)
        player = mixer.blend(Player, username=request.user,
                             colour='Rojo',
                             development_cards=1,
                             resources_cards=5)
        hexe_position = HexePosition.objects.create(level=1, index=2)

        request.board = Board.objects.create(name='Colonos')

        game = Game.objects.create(name='Juego', board=request.board,
                                   robber=hexe_position, winner=request.user)

        resource_list = []
        card_list = []

        resource = mixer.blend(Resource, owner=player,
                               game=game, resource_name="ore")

        card = mixer.blend(Card, owner=player,
                           game=game, card_name="monopoly")

        resource_list.append(resource.resource_name)

        card_list.append(card.card_name)

        view = PlayerInfo.as_view()
        response = view(request, pk=1)
        assert response.status_code == 200
