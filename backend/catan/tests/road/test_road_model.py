import pytest
from catan.models import *
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestModels:
    def test_road(self):
        user = User.objects.create_user(username='nvero', password='barco12')
        board = Board.objects.create(name="Colonos")
        hexe_pos = HexePosition.objects.create(level=0, index=0)
        vertex_pos1 = VertexPosition.objects.create(level=1, index=17)
        vertex_pos2 = VertexPosition.objects.create(level=2, index=1)
        game = Game.objects.create(name="Game1", board=board,
                                   robber=hexe_pos)
        player = Player.objects.create(turn=1, username=user,
                                       game=game, colour="red")
        road = Road.objects.create(owner=player,
                                   vertex_1=vertex_pos1,
                                   vertex_2=vertex_pos2,
                                   game=game)

        assert player == road.owner
        assert vertex_pos1 == road.vertex_1
        assert vertex_pos2 == road.vertex_2
        assert game == road.game
