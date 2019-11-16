from django.test import TestCase, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from catan.models import *
from catan.views.players_views import PlayerActions
from aux.generateBoard import *
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest


@pytest.mark.django_db
class TestViews(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        self.token = AccessToken()

    def createGame(self):
        self.user1 = mixer.blend(User, username='user1', password='1234')
        self.user2 = mixer.blend(User, username='user2', password='1234')
        self.user3 = mixer.blend(User, username='user3', password='1234')
        self.user4 = mixer.blend(User, username='user4', password='1234')

        generateHexesPositions()
        generateVertexPositions()

        self.board = generateBoard('colones')
        self.room = Room.objects.create(
            name='Room1', owner=self.user1, board_id=1)

        self.hexe_position = HexePosition.objects.all()[0]

        self.game = Game.objects.create(name='Game1', board=self.board,
                                        robber=self.hexe_position)
        self.player1 = mixer.blend(Player, username=self.user1,
                                   game=self.game, colour='yellow')
        self.player2 = mixer.blend(Player, username=self.user2,
                                   game=self.game, colour='green')
        self.player3 = mixer.blend(Player, username=self.user3,
                                   game=self.game, colour='blue')
        self.player4 = mixer.blend(Player, username=self.user4,
                                   game=self.game, colour='red')

    def test_ActionsNotInTurn(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user2, game=self.game,
            dices1=4, dices2=3)

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'move_robber',
                'payload': {
                    'position': {
                        'level': 2,
                        'index': 10
                    },
                    'player': ''
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
        assert response.data == {"detail": "Not in turn"}

    def test_ActionsInvalid(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=3)

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': '1234',
                'payload': {
                    'position': {
                        'level': 2,
                        'index': 10
                    },
                    'player': ''
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
        assert response.data == {"detail": 'Please select a valid action'}

    def test_positionInvalid(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=3)

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'move_robber',
                'payload': {
                    'position': {
                        'level': 6,
                        'index': 10
                    },
                    'player': ''
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
        assert response.data == {
            "detail": "There is no hexagon in that position"}

    def test_DicesNot7(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=4)

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'move_robber',
                'payload': {
                    'position': {
                        'level': 2,
                        'index': 10
                    },
                    'player': ''
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
        assert response.data == {"detail": "the dices don't give 7"}

    def test_move_robberWithOutBuildings(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=3)

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'move_robber',
                'payload': {
                    'position': {
                        'level': 2,
                        'index': 10
                    },
                    'player': ''
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        assert response.data == {
            "detail": "there are no buildings in the hexagon"}
        assert Game.objects.filter(
            robber=HexePosition.objects.all()[17]).exists() is True

    def test_move_robberOneBuilding(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=3)

        vertex_positions = VertexPosition.objects.all()
        building1 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player2, position=vertex_positions[21])

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'move_robber',
                'payload': {
                    'position': {
                        'level': 2,
                        'index': 10
                    },
                    'player': ''
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        assert response.data == {"detail": "the player has no resources"}

        resources = Resource.objects.create(
            owner=self.player2, game=self.game, resource_name='ore')

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        assert response.data == {"detail": "you stole the resource ore"}

    def test_move_robberMyOneBuilding(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=3)

        vertex_positions = VertexPosition.objects.all()
        building1 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player1, position=vertex_positions[21])

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'move_robber',
                'payload': {
                    'position': {
                        'level': 2,
                        'index': 10
                    },
                    'player': ''
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        assert response.data == {
            "detail": "there are no enemy buildings in the hexagon"}

    def test_move_robberMoreBuildings(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=3)

        vertex_positions = VertexPosition.objects.all()
        building1 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player2, position=vertex_positions[21])
        building2 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player3, position=vertex_positions[49])

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'move_robber',
                'payload': {
                    'position': {
                        'level': 2,
                        'index': 10
                    },
                    'player': 'user2'
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        assert response.data == {"detail": "the player has no resources"}

        resources = Resource.objects.create(
            owner=self.player2, game=self.game, resource_name='ore')

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        assert response.data == {"detail": "you stole the resource ore"}

        data = {'type': 'move_robber',
                'payload': {
                    'position': {
                        'level': 2,
                        'index': 10
                    },
                    'player': 'user4'
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
        assert response.data == {
            "detail": "you have to choose a player that has buildings"}

        data = {'type': 'move_robber',
                'payload': {
                    'position': {
                        'level': 2,
                        'index': 10
                    },
                    'player': 'user1'
                }
                }

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
        assert response.data == {"detail": "you can't choose yourself"}

    def test_get_robberPositions(self):
        self.createGame()
        new_robber = HexePosition.objects.get(level=1, index=0)
        self.game.robber = new_robber
        self.game.save()
        current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=3, game_stage='full_play')
        position1 = VertexPosition.objects.get(level=2, index=5)
        position2 = VertexPosition.objects.get(level=1, index=17)
        position3 = VertexPosition.objects.get(level=0, index=0)
        position4 = VertexPosition.objects.get(level=1, index=15)
        Building.objects.create(game=self.game,
                                owner=self.player1,
                                name='city',
                                position=position1)
        Building.objects.create(game=self.game,
                                owner=self.player2,
                                name='city',
                                position=position2)
        Building.objects.create(game=self.game,
                                owner=self.player2,
                                name='settlement',
                                position=position3)
        Building.objects.create(game=self.game,
                                owner=self.player3,
                                name='settlement',
                                position=position4)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expeceted_data = [
            {'payload': [
                {'players': ['user2'], 'position': {'level': 0, 'index': 0}},
                {'players': [], 'position': {'level': 1, 'index': 1}},
                {'players': [], 'position': {'level': 1, 'index': 2}},
                {'players': [], 'position': {'level': 1, 'index': 3}},
                {'players': ['user3'], 'position': {'level': 1, 'index': 4}},
                {'players': ['user2', 'user3'], 'position': {'level': 1,
                                                             'index': 5}},
                {'players': ['user2'], 'position': {'level': 2, 'index': 0}},
                {'players': [], 'position': {'level': 2, 'index': 1}},
                {'players': ['user1'], 'position': {'level': 2, 'index': 2}},
                {'players': [], 'position': {'level': 2, 'index': 3}},
                {'players': [], 'position': {'level': 2, 'index': 4}},
                {'players': [], 'position': {'level': 2, 'index': 5}},
                {'players': [], 'position': {'level': 2, 'index': 6}},
                {'players': [], 'position': {'level': 2, 'index': 7}},
                {'players': [], 'position': {'level': 2, 'index': 8}},
                {'players': [], 'position': {'level': 2, 'index': 9}},
                {'players': ['user3'], 'position': {'level': 2, 'index': 10}},
                {'players': ['user2'], 'position': {'level': 2, 'index': 11}}],
             'type': 'move_robber'}]
        assert response.data == expeceted_data
        assert response.status_code == 200

    def test_get_robberPositions_not_7(self):
        self.createGame()
        new_robber = HexePosition.objects.get(level=1, index=0)
        self.game.robber = new_robber
        self.game.save()
        current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=1, dices2=3, game_stage='full_play')
        position1 = VertexPosition.objects.get(level=2, index=5)
        position2 = VertexPosition.objects.get(level=1, index=17)
        position3 = VertexPosition.objects.get(level=0, index=0)
        position4 = VertexPosition.objects.get(level=1, index=15)
        Building.objects.create(game=self.game,
                                owner=self.player1,
                                name='city',
                                position=position1)
        Building.objects.create(game=self.game,
                                owner=self.player2,
                                name='city',
                                position=position2)
        Building.objects.create(game=self.game,
                                owner=self.player2,
                                name='settlement',
                                position=position3)
        Building.objects.create(game=self.game,
                                owner=self.player3,
                                name='settlement',
                                position=position4)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.data == []
        assert response.status_code == 200

    def test_get_robberPositions_not_Buildings(self):
        self.createGame()
        new_robber = HexePosition.objects.get(level=1, index=0)
        self.game.robber = new_robber
        self.game.save()
        current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=1, dices2=6, game_stage='full_play')
        position1 = VertexPosition.objects.get(level=2, index=5)
        position2 = VertexPosition.objects.get(level=1, index=17)
        position3 = VertexPosition.objects.get(level=0, index=0)
        position4 = VertexPosition.objects.get(level=1, index=15)
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = [
            {'payload': [
                {'players': [], 'position': {'level': 0, 'index': 0}},
                {'players': [], 'position': {'level': 1, 'index': 1}},
                {'players': [], 'position': {'level': 1, 'index': 2}},
                {'players': [], 'position': {'level': 1, 'index': 3}},
                {'players': [], 'position': {'level': 1, 'index': 4}},
                {'players': [], 'position': {'level': 1, 'index': 5}},
                {'players': [], 'position': {'level': 2, 'index': 0}},
                {'players': [], 'position': {'level': 2, 'index': 1}},
                {'players': [], 'position': {'level': 2, 'index': 2}},
                {'players': [], 'position': {'level': 2, 'index': 3}},
                {'players': [], 'position': {'level': 2, 'index': 4}},
                {'players': [], 'position': {'level': 2, 'index': 5}},
                {'players': [], 'position': {'level': 2, 'index': 6}},
                {'players': [], 'position': {'level': 2, 'index': 7}},
                {'players': [], 'position': {'level': 2, 'index': 8}},
                {'players': [], 'position': {'level': 2, 'index': 9}},
                {'players': [], 'position': {'level': 2, 'index': 10}},
                {'players': [], 'position': {'level': 2, 'index': 11}}],
             'type': 'move_robber'}
        ]
        assert response.data == expected_data
        assert response.status_code == 200
