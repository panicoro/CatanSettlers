from django.test import TestCase, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from catan.models import *
from catan.views import PlayerInfo
from catan.dices import *
from aux.generateBoard import *
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import json


@pytest.mark.django_db
class TestView(TestCase):

    def test_random_discard(self):
        board = mixer.blend('catan.Board', name="board1")
        robber = mixer.blend('catan.HexePosition', level=0, index=0)
        game = mixer.blend('catan.Game', name="game1", board=board,
                           robber=robber)
        username1 = mixer.blend(User, username="player_test1",
                                password="prueba")
        username2 = mixer.blend(User, username="player_test2",
                                password="prueba")
        username3 = mixer.blend(User, username="player_test3",
                                password="prueba")
        username4 = mixer.blend(User, username="player_test4",
                                password="prueba")
        player1 = mixer.blend("catan.Player", turn=1, username=username1,
                              game=game, colour="yellow", resources_cards=6)
        player2 = mixer.blend("catan.Player", turn=2, username=username2,
                              game=game, colour="blue", resources_cards=9)
        player3 = mixer.blend("catan.Player", turn=3, username=username3,
                              game=game, colour="green", resources_cards=7)
        player4 = mixer.blend("catan.Player", turn=4, username=username4,
                              game=game, colour="red", resources_cards=2)
        for i in range(3):
            mixer.blend("catan.Resource", game=game,
                        resource_name="grain", owner=player1)
            mixer.blend("catan.Resource", game=game,
                        resource_name="brick", owner=player1)
            mixer.blend("catan.Resource", game=game,
                        resource_name="wool", owner=player2)
            mixer.blend("catan.Resource", game=game,
                        resource_name="ore", owner=player2)
            mixer.blend("catan.Resource", game=game,
                        resource_name="lumber", owner=player2)
            mixer.blend("catan.Resource", game=game,
                        resource_name="lumber", owner=player3)
        for i in range(2):
            mixer.blend("catan.Resource", game=game,
                        resource_name="ore", owner=player3)
            mixer.blend("catan.Resource", game=game,
                        resource_name="wool", owner=player3)
            mixer.blend("catan.Resource", game=game,
                        resource_name="lumber", owner=player4)
        path = reverse('PlayerInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        token = AccessToken()
        force_authenticate(request, user=username1, token=token)
        view = PlayerInfo.as_view()
        response = view(request, pk=1)
        assert player1.resources_cards == 6
        assert response.data == {
                                 'cards': [],
                                 'resources': [
                                     'grain',
                                     'brick',
                                     'grain',
                                     'brick',
                                     'grain',
                                     'brick']
                                }
        force_authenticate(request, user=username2, token=token)
        view = PlayerInfo.as_view()
        response = view(request, pk=1)
        assert player2.resources_cards == 9
        assert response.data == {
                                 'cards': [],
                                 'resources': [
                                     'wool',
                                     'ore',
                                     'lumber',
                                     'wool',
                                     'ore',
                                     'lumber',
                                     'wool',
                                     'ore',
                                     'lumber']
                                }
        force_authenticate(request, user=username3, token=token)
        view = PlayerInfo.as_view()
        response = view(request, pk=1)
        assert player3.resources_cards == 7
        assert response.data == {
                                 'cards': [],
                                 'resources': [
                                     'lumber',
                                     'lumber',
                                     'lumber',
                                     'ore',
                                     'wool',
                                     'ore',
                                     'wool']
                                }
        force_authenticate(request, user=username4, token=token)
        view = PlayerInfo.as_view()
        response = view(request, pk=1)
        assert player4.resources_cards == 2
        assert response.data == {
                                 'cards': [],
                                 'resources': [
                                     'lumber',
                                     'lumber']
                                }
        players = Player.objects.filter(game=game)
        random_discard(players)
        assert Player.objects.filter(username=username1,
                                     game=game)[0].resources_cards == 6
        assert Player.objects.filter(username=username2,
                                     game=game)[0].resources_cards == 5
        assert Player.objects.filter(username=username3,
                                     game=game)[0].resources_cards == 7
        assert Player.objects.filter(username=username4,
                                     game=game)[0].resources_cards == 2
