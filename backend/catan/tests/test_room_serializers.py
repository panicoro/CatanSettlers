from mixer.backend.django import mixer
from catan.serializers import UserSerializer, RoomSerializer
from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
class TestSerializer:

    def test_userSerializer(self):
        user = mixer.blend(User, username="owner_test", password="hola1234")
        serializer = UserSerializer(user)
        data = serializer.data
        assert data['username'] == user.username

    def test_userSerializerData(self):
        user_data = {'username': 'test_name', 'password': 'hola1234'}
        serializer = UserSerializer(data=user_data)
        assert serializer.is_valid() == True
        data = serializer.validated_data
        assert data['username'] == user_data['username']

    def test_RoomSerializer(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        player2 = mixer.blend(User, username="player_test2",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)
        room.players.add(player1)
        room.players.add(player2)
        serializer = RoomSerializer(room)
        data = serializer.data
        assert data['owner']['username'] == owner.username
        assert data['max_players'] == room.max_players
        assert data['name'] == room.name
        for player in data['players']:
            assert room.players.filter(username=player['username']
                                       ).exists() == True

    def test_RoomSerializerData(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        player2 = mixer.blend(User, username="player_test2",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)
        room.players.add(player1)
        room_data = {
            "name": "Test Room",
            "max_players": 3,
            "owner": {
                "username": "owner_test"
            },
            "players": [{
                "username": "player_test1"
            }, {
                "username": "player_test2"
            }]
        }
        serializer = RoomSerializer(room, data=room_data)
        assert serializer.is_valid() == True
        data = serializer.validated_data
        assert data['name'] == room_data['name']
        assert data['owner']['username'] == room_data['owner']['username']
        assert data['max_players'] == room_data['max_players']
        assert data['players'] == room_data['players']
