from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from catan.views import RoomList, RoomDetail
import pytest
import json


@pytest.mark.django_db
class TestView:

    def test_listEmptyRoomAuthenticated(self):
        path = reverse('list_rooms')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        view = RoomList.as_view()
        response = view(request)
        response.render()
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 0

    def test_listRoomAuthenticated(self):
        path = reverse('list_rooms')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        room_1 = mixer.blend('catan.Room')
        room_2 = mixer.blend('catan.Room')
        view = RoomList.as_view()
        response = view(request)
        response.render()
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2

    def test_listRoomNotAuthenticated(self):
        path = reverse('list_rooms')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        room_1 = mixer.blend('catan.Room')
        view = RoomList.as_view()
        response = view(request)
        response.render()
        assert response.status_code == 401
        assert len(json.loads(response.content)) == 0

    def test_roomDetailOwner(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)

        path = reverse('join_room', kwargs={'pk': 1})
        data = {
            'id': 1,
            'name': 'Test Room',
            'max_players': 3,
            'owner': {'username': 'owner_test'},
            'players': [{'username': 'player_test1'}]
        }
        request = RequestFactory().put(path, data,
                                       content_type='application/json')
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 200
        assert json.loads(response.content) == data

    def test_roomDetailNotOwner(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)

        path = reverse('join_room', kwargs={'pk': 1})
        data = {
            'id': 1,
            'name': 'Test Room',
            'max_players': 3,
            'owner': {'username': 'owner_test'},
            'players': [{'username': 'player_test1'}]
        }
        request = RequestFactory().put(path, data,
                                       content_type='application/json')
        request.user = mixer.blend(User, username='NoOwner',
                                   password='hola1234')
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 403

    def test_changeRoomName(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)
        path = reverse('join_room', kwargs={'pk': 1})
        data = {
            'id': 1,
            'name': 'Change name of the room',
            'max_players': 3,
            'owner': {'username': 'owner_test'},
            'players': [{'username': 'player_test1'}]
        }
        request = RequestFactory().put(path, data,
                                       content_type='application/json')
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 400

    def test_changeRoomMaxPlayers(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)

        path = reverse('join_room', kwargs={'pk': 1})
        data = {
            'id': 1,
            'name': 'Test room',
            'max_players': 4,
            'owner': {'username': 'owner_test'},
            'players': [{'username': 'player_test1'}]
        }
        request = RequestFactory().put(path, data,
                                       content_type='application/json')
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 400

    def test_addtoManyPlayers(self):
        owner = mixer.blend(User, username="owner_test",
                            password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        player2 = mixer.blend(User, username="player_test2",
                              password="hola1234")
        player3 = mixer.blend(User, username="player_test3",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)
        path = reverse('join_room', kwargs={'pk': 1})
        data = {
            'id': 1,
            'name': 'Test room',
            'max_players': 3,
            'owner': {'username': 'owner_test'},
            'players': [{'username': 'player_test1'},
                        {'username': 'player_test2'},
                        {'username': 'player_test3'}
                        ]
        }
        request = RequestFactory().put(path, data,
                                       content_type='application/json')
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 400

    def test_addIdemPlayers(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)
        path = reverse('join_room', kwargs={'pk': 1})
        data = {
            'id': 1,
            'name': 'Test room',
            'max_players': 3,
            'owner': {'username': 'owner_test'},
            'players': [{'username': 'player_test1'},
                        {'username': 'player_test1'}
                        ]
        }
        request = RequestFactory().put(path, data,
                                       content_type='application/json')
        view = RoomDetail.as_view()
        response = view(request, pk=1)
        response.render()
        assert response.status_code == 400
