import pytest
from catan.models import *
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:
    def test_building(self):
        user1 = User.objects.create_user(username='user1', password='hola1234')
        board = Board.objects.create(name="Board1")
        hexe_pos = HexePosition.objects.create(level=1, index=2)
        vertex_pos = VertexPosition.objects.create(level=0, index=4)
        game1 = Game.objects.create(name="Game1", board=board,
                                    robber=hexe_pos)
        game2 = Game.objects.create(name="Game2", board=board,
                                    robber=hexe_pos)
        player1 = Player.objects.create(turn=1, username=user1,
                                        game=game2, colour="blue")
        building = Building.objects.create(
            name="settlement", game=game1, owner=player1,
            position=vertex_pos)
        try:
            building.full_clean()
        except ValidationError as e:
            error = 'Cannot be player of other game'
            assert error in e.message_dict['__all__']
