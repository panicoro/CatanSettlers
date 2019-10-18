from mixer.backend.django import mixer
from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
class TestModels:

    def test_createRoom(self):
        owner = mixer.blend(User, username="owner_test", password="hola1234")
        player1 = mixer.blend(User, username="player_test1",
                              password="hola1234")
        player2 = mixer.blend(User, username="player_test2",
                              password="hola1234")
        room = mixer.blend('catan.Room', name="Test Room", max_players=3,
                           owner=owner)
        room.players.add(player1)
        room.players.add(player2)
        assert room.max_players == 3
        assert room.name == "Test Room"
        assert str(room) == "Test Room"
        assert room.owner == owner
        assert room.players.filter(username=player1.username
                                   ).exists() is True
        assert room.players.filter(username=player2.username
                                   ).exists() is True
