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
        board = mixer.blend('catan.Board', name='test_board')
        room = mixer.blend('catan.Room', name="Test Room", max_players=4,
                           owner=owner, board_id=board.id)
        room.players.add(player1)
        room.players.add(player2)
        assert room.max_players == 4
        assert room.name == "Test Room"
        assert room.game_id is None
        assert room.board_id == board.id
        assert room.owner == owner
        assert room.game_has_started is False
        assert room.players.filter(username=player1.username
                                   ).exists() is True
        assert room.players.filter(username=player2.username
                                   ).exists() is True
