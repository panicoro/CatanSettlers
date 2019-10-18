from mixer.backend.django import mixer
from catan.serializers import RoomSerializer
from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
class TestSerializer:

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
        assert data['owner'] == owner.username
        assert data['max_players'] == room.max_players
        assert data['name'] == room.name
        for player_data in data['players']:
            assert room.players.filter(username=player_data
                                       ).exists() is True

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
            "owner": "owner_test",
            "players": ["player_test1", "player_test2"]
        }
        serializer = RoomSerializer(room, data=room_data)
        assert serializer.is_valid() is True
        serializer.save()
        data = serializer.data
        assert data['name'] == room_data['name']
        assert data['owner'] == room_data['owner']
        assert data['max_players'] == room_data['max_players']
        assert data['players'] == room_data['players']

    def test_RoomSerializerDataValidatePlayers(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        player2 = mixer.blend(User, username="player_test2",
                              password="hola1234")
        player3 = mixer.blend(User, username="player_test3",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)
        room.players.add(player1)
        room.players.add(player2)
        room_data = {
            "name": "Test Room",
            "max_players": 3,
            "owner": "owner_test",
            "players": ["player_test1", "player_test2", "player_test3"]
        }
        serializer = RoomSerializer(room, data=room_data)
        assert serializer.is_valid() is False

    def test_RoomSerializerDataValidateOwner(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)
        room.players.add(player1)
        room_data = {
            "name": "Test Room",
            "max_players": 3,
            "owner": "owner_test",
            "players": ["player_test1", "owner_test"]
        }
        serializer = RoomSerializer(room, data=room_data)
        assert serializer.is_valid() is False
