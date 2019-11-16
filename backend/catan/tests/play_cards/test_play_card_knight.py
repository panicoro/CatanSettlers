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
        self.expected_payload = {
            'payload': [
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
        }

    def createGame(self):
        self.user1 = mixer.blend(User, username='user1', password='1234')
        self.user2 = mixer.blend(User, username='user2', password='1234')
        self.user3 = mixer.blend(User, username='user3', password='1234')
        self.user4 = mixer.blend(User, username='user4', password='1234')

        generateHexesPositions()
        generateVertexPositions()

        self.board = generateBoard('Board1')
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

    def test_positionInvalid(self):
        self.createGame()
        self.current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=4, dices2=3)
        card = Card.objects.create(owner=self.player1,
                                   game=self.game,
                                   card_name='knight')

        path = reverse('PlayerActions', kwargs={'pk': 1})

        data = {'type': 'play_knight_card',
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

    def test_get_robberPositions(self):
        self.createGame()
        new_robber = HexePosition.objects.get(level=1, index=0)
        self.game.robber = new_robber
        self.game.save()
        current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=6, dices2=3, game_stage='full_play')
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
        Card.objects.create(owner=self.player1,
                            game=self.game,
                            card_name='knight')
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expeceted_data = []
        self.expected_payload['type'] = 'play_knight_card'
        expeceted_data.append(self.expected_payload)
        assert response.data == expeceted_data
        assert response.status_code == 200

    def test_get_robberPositions_Mix(self):
        self.createGame()
        new_robber = HexePosition.objects.get(level=1, index=0)
        self.game.robber = new_robber
        self.game.save()
        current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=6, dices2=1, game_stage='full_play')
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
        Card.objects.create(owner=self.player1,
                            game=self.game,
                            card_name='knight')
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expected_data = []
        move_robber = self.expected_payload
        move_robber['type'] = 'move_rober'
        expected_data.append(move_robber)
        play_card = self.expected_payload
        play_card['type'] = 'play_knight_card'
        expected_data.append(play_card)
        assert move_robber in response.data
        assert play_card in response.data
        assert response.status_code == 200

    def test_get_robberPositions_NoBuildings(self):
        self.createGame()
        new_robber = HexePosition.objects.get(level=1, index=0)
        self.game.robber = new_robber
        self.game.save()
        current_turn = mixer.blend(
            Current_Turn, user=self.user1, game=self.game,
            dices1=6, dices2=3, game_stage='full_play')
        position1 = VertexPosition.objects.get(level=2, index=5)
        position2 = VertexPosition.objects.get(level=1, index=17)
        position3 = VertexPosition.objects.get(level=0, index=0)
        position4 = VertexPosition.objects.get(level=1, index=15)
        Card.objects.create(owner=self.player1,
                            game=self.game,
                            card_name='knight')
        path = reverse('PlayerActions', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user1, token=self.token)
        view = PlayerActions.as_view()
        response = view(request, pk=1)
        expeceted_data = [
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
             'type': 'play_knight_card'}]
        assert response.data == expeceted_data
        assert response.status_code == 200

    def test_get_robberPositions_NoCard(self):
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
