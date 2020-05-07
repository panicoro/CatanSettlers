from django.test import TestCase, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from catan.models import *
from catan.views.room_views import RoomList, RoomDetail
from aux.generateBoard import *
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import json


@pytest.mark.django_db
class TestViewRoom(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@example.com'
        self.user = mixer.blend(User, username=self.username, email=self.email)
        self.token = AccessToken()
        self.owner = mixer.blend(User, username="owner_test",
                                 password="hola1234")
        self.player_1 = mixer.blend(User, username="player_test1",
                                    password="hola1234")
        self.player_2 = mixer.blend(User, username="player_test2",
                                    password="hola1234")
        self.player_3 = mixer.blend(User, username="player_test3",
                                    password="hola1234")
        self.board = mixer.blend('catan.Board', name='board_name')
        self.room_1 = mixer.blend('catan.Room', owner=self.owner,
                                  board_id=self.board.id,
                                  name='room_1')
        self.room_2 = mixer.blend('catan.Room', owner=self.owner,
                                  board_id=self.board.id,
                                  name='room_2')
        self.room_1.players.add(self.owner)
        self.room_2.players.add(self.owner)
        self.room_1.players.add(self.player_1)
        self.room_1.players.add(self.player_2)
        self.room_2.players.add(self.player_2)

    def test_list_empty_room_authenticated(self):
        self.room_1.delete()
        self.room_2.delete()
        path = reverse('list_rooms')
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomList.as_view()
        response = view(request)
        response.render()
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 0

    def test_list_room_authenticated(self):
        path = reverse('list_rooms')
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomList.as_view()
        response = view(request)
        assert response.status_code == 200
        json_1 = {'board_id': 1, 'game_has_started': False,
                  'game_id': None, 'id': 1, 'max_players': 4,
                  'name': 'room_1', 'owner': 'owner_test',
                  'players': ['owner_test', 'player_test1',
                              'player_test2']}
        json_2 = {'board_id': 1, 'game_has_started': False,
                  'game_id': None, 'id': 2, 'max_players': 4,
                  'name': 'room_2', 'owner': 'owner_test',
                  'players': ['owner_test', 'player_test2']}
        assert json_1 in response.data
        assert json_2 in response.data

    def test_list_room_not_authenticated(self):
        path = reverse('list_rooms')
        request = RequestFactory().get(path)
        room_1 = mixer.blend('catan.Room')
        view = RoomList.as_view()
        response = view(request)
        assert response.status_code == 401

    def test_view_room(self):
        path = reverse('join_room', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        json_1 = {'game_has_started': False,
                  'game_id': None, 'id': 1, 'max_players': 4,
                  'name': 'room_1', 'owner': 'owner_test',
                  'players': ['owner_test', 'player_test1',
                              'player_test2']}
        assert json_1 == response.data
        assert response.status_code == 200

    def test_add_to_many_players(self):
        self.room_1.players.add(self.player_3)
        path = reverse('join_room', kwargs={'pk': 1})
        request = RequestFactory().put(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        assert len(self.room_1.players.all()) == 4
        assert response.status_code == 400
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        json_1 = {'game_has_started': False,
                  'game_id': None, 'id': 1, 'max_players': 4,
                  'name': 'room_1', 'owner': 'owner_test',
                  'players': ['owner_test', 'player_test1',
                              'player_test2', 'player_test3']}
        assert json_1 == response.data
        assert response.status_code == 200

    def test_add_players_inexistent_room(self):
        self.room_1.delete()
        path = reverse('join_room', kwargs={'pk': 1})
        request = RequestFactory().put(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 404

    def test_add_players(self):
        path = reverse('join_room', kwargs={'pk': 2})
        request = RequestFactory().put(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=2)
        assert response.status_code == 204
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=2)
        json_1 = {'game_has_started': False,
                  'game_id': None, 'id': 2, 'max_players': 4,
                  'name': 'room_2', 'owner': 'owner_test',
                  'players': ['test_user', 'owner_test',
                              'player_test2']}
        assert json_1 == response.data
        assert response.status_code == 200

    def test_create_room_success(self):
        path = reverse('list_rooms')
        data = {'name': 'room_3', 'owner': self.user.username,
                'players': [], 'board_id': self.board.id}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomList.as_view()
        response = view(request)
        assert response.status_code == 201
        path = reverse('join_room', kwargs={'pk': 3})
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=3)
        json_1 = {'game_has_started': False,
                  'game_id': None, 'id': 3, 'max_players': 4,
                  'name': 'room_3', 'owner': 'test_user',
                  'players': ['test_user']}
        assert json_1 == response.data
        assert response.status_code == 200

    def test_create_room_whitout_data(self):
        path = reverse('list_rooms')
        data = {}
        request = RequestFactory().post(path, data,
                                        content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomList.as_view()
        response = view(request)
        assert response.status_code == 405

    def test_start_game(self):
        desert = mixer.blend('catan.Hexe', board=self.board,
                             terrain='desert')
        self.room_1.players.add(self.player_3)
        path = reverse('join_room', kwargs={'pk': 1})
        request = RequestFactory().patch(path,
                                         content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        request = RequestFactory().get(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        json_1 = {'game_has_started': True,
                  'game_id': 1, 'id': 1, 'max_players': 4,
                  'name': 'room_1', 'owner': 'owner_test',
                  'players': ['owner_test', 'player_test1',
                              'player_test2',
                              'player_test3']}
        assert json_1 == response.data
        assert response.status_code == 200

    def test_start_game_without_all_players(self):
        path = reverse('join_room', kwargs={'pk': 1})
        request = RequestFactory().patch(path,
                                         content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        assert response.status_code == 400

    def test_delete_room(self):
        path = reverse('join_room', kwargs={'pk': 1})
        request = RequestFactory().delete(path)
        force_authenticate(request, user=self.owner, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        assert Room.objects.filter(id=1).exists() is False

    def test_delete_room_not_owner(self):
        path = reverse('join_room', kwargs={'pk': 1})
        request = RequestFactory().delete(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
        assert response.data == {
            "detail": "Can't delete the room"}
        assert Room.objects.filter(id=1).exists() is True

    def test_delete_room_has_tarted(self):
        desert = mixer.blend('catan.Hexe', board=self.board,
                             terrain='desert')
        self.room_1.players.add(self.player_3)
        path = reverse('join_room', kwargs={'pk': 1})
        request = RequestFactory().patch(path,
                                         content_type='application/json')
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        assert response.status_code == 204
        path = reverse('join_room', kwargs={'pk': 1})
        request = RequestFactory().delete(path)
        force_authenticate(request, user=self.user, token=self.token)
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        assert response.status_code == 403
        assert response.data == {
            "detail": "Can't delete the room"}
        assert Room.objects.filter(id=1).exists() is True
