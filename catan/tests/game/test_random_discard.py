from django.test import TestCase, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from catan.models import *
from catan.views.players_views import PlayerInfo
from aux.generateBoard import *
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import json


@pytest.mark.django_db
class TestView(TestCase):

    def test_random_discard(self):
        board = mixer.blend('catan.Board', name="board1")
        robber = mixer.blend('catan.Hexe', level=0, index=0)
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
                        name="grain", owner=player1)
            mixer.blend("catan.Resource", game=game,
                        name="brick", owner=player1)
            mixer.blend("catan.Resource", game=game,
                        name="wool", owner=player2)
            mixer.blend("catan.Resource", game=game,
                        name="ore", owner=player2)
            mixer.blend("catan.Resource", game=game,
                        name="lumber", owner=player2)
            mixer.blend("catan.Resource", game=game,
                        name="lumber", owner=player3)
        for i in range(2):
            mixer.blend("catan.Resource", game=game,
                        name="ore", owner=player3)
            mixer.blend("catan.Resource", game=game,
                        name="wool", owner=player3)
            mixer.blend("catan.Resource", game=game,
                        name="lumber", owner=player4)
        path = reverse('PlayerInfo', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        token = AccessToken()
        force_authenticate(request, user=username1, token=token)
        view = PlayerInfo.as_view()
        response = view(request, pk=1)
        assert len(response.data['resources']) == 6
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
        assert len(response.data['resources']) == 9
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
        assert len(response.data['resources']) == 7
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
        assert len(response.data['resources']) == 2
        assert response.data == {
                                 'cards': [],
                                 'resources': [
                                     'lumber',
                                     'lumber']
                                }
        players = Player.objects.filter(game=game)
        game.random_discard()
        assert len(Resource.objects.filter(owner=player1)) == 6
        assert len(Resource.objects.filter(owner=player2)) == 5
        assert len(Resource.objects.filter(owner=player3)) == 7
        assert len(Resource.objects.filter(owner=player4)) == 2
