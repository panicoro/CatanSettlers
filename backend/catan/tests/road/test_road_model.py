import pytest
from catan.models import *
from mixer.backend.django import mixer
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestModels:
    def test_road(self):
        user = mixer.blend(User, username='nvero', password='barco12')
        board = mixer.blend('catan.Board', name="Colonos")
        hexe_pos = mixer.blend('catan.Hexe', terrain='desert', token=2,
                               board=board)
        game = mixer.blend('catan.Game', name="Game1", board=board,
                           robber=hexe_pos)
        player = mixer.blend('catan.Player', turn=1, username=user,
                             game=game, colour="red")
        road = mixer.blend('catan.Road', owner=player,
                           level_1=1, index_1=16,
                           level_2=2, index_2=26,
                           game=game)
        assert player == road.owner
        assert (1, 16) == (road.level_1, road.index_1)
        assert (2, 26) == (road.level_2, road.index_2)
        assert game == road.game

    def test_vertex_position_not_valid(self):
        user = mixer.blend(User, username='nvero', password='barco12')
        board = mixer.blend('catan.Board', name="Colonos")
        hexe_pos = mixer.blend('catan.Hexe', terrain='desert', token=2,
                               board=board)
        game = mixer.blend('catan.Game', name="Game1", board=board,
                           robber=hexe_pos)
        player = mixer.blend('catan.Player', turn=1, username=user,
                             game=game, colour="red")
        road = mixer.blend('catan.Road', owner=player,
                           level_1=0, index_1=16,
                           level_2=2, index_2=26,
                           game=game)
        try:
            road.full_clean()
        except ValidationError as e:
            error = 'The index with level 0 must be between 0 and 5.'
            assert error in e.message_dict['__all__']
        road = mixer.blend('catan.Road', owner=player,
                           level_1=1, index_1=18,
                           level_2=2, index_2=26,
                           game=game)
        try:
            road.full_clean()
        except ValidationError as e:
            error = 'The index with level 1 must be between 0 and 17.'
            assert error in e.message_dict['__all__']
        road = mixer.blend('catan.Road', owner=player,
                           level_1=1, index_1=16,
                           level_2=2, index_2=30,
                           game=game)
        try:
            road.full_clean()
        except ValidationError as e:
            error = 'The index with level 2 must be between 0 and 29.'
            assert error in e.message_dict['__all__']
