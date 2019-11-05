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

        self.board = Board.objects.create(name='Board1')
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
            Current_Turn, user=self.user2, game=self.game)

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'play_knight_card',
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

    def test_move_robberWithOutBuildings(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game)
        card = Card.objects.create(owner=self.player1,
                                   game=self.game,
                                   card_name='knight')

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'play_knight_card',
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
            Current_Turn, user=self.user1, game=self.game)

        vertex_positions = VertexPosition.objects.all()
        building1 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player2, position=vertex_positions[21])
        Card.objects.create(owner=self.player1,
                            game=self.game,
                            card_name='knight')
        Card.objects.create(owner=self.player1,
                            game=self.game,
                            card_name='knight')

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'play_knight_card',
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
            Current_Turn, user=self.user1, game=self.game)

        vertex_positions = VertexPosition.objects.all()
        building1 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player1, position=vertex_positions[21])
        card = Card.objects.create(owner=self.player1,
                                   game=self.game,
                                   card_name='knight')

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'play_knight_card',
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
            Current_Turn, user=self.user1, game=self.game)

        vertex_positions = VertexPosition.objects.all()
        building1 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player2, position=vertex_positions[21])
        building2 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player3, position=vertex_positions[49])
        Card.objects.create(owner=self.player1,
                            game=self.game,
                            card_name='knight')
        Card.objects.create(owner=self.player1,
                            game=self.game,
                            card_name='knight')
        Card.objects.create(owner=self.player1,
                            game=self.game,
                            card_name='knight')

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'play_knight_card',
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
#        assert response.data == {"detail": "the player has no resources"}

        resources = Resource.objects.create(
            owner=self.player2, game=self.game, resource_name='ore')

        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        assert response.data == {"detail": "you stole the resource ore"}

        data = {'type': 'play_knight_card',
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

        data = {'type': 'play_knight_card',
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

    def test_playCardKnight(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game)

        vertex_positions = VertexPosition.objects.all()
        building1 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player2, position=vertex_positions[21])
        card = Card.objects.create(owner=self.player1,
                                   game=self.game,
                                   card_name='knight')

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'play_knight_card',
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

    def test_noHaveKnightCards(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game)

        vertex_positions = VertexPosition.objects.all()
        building1 = Building.objects.create(
            name="settlement", game=self.game,
            owner=self.player2, position=vertex_positions[21])

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'play_knight_card',
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
        assert response.data == {"detail": "You have no knight cards"}
