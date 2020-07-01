import pytest
from catan.models import *
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:
    def test_building(self):
        user_1 = mixer.blend(User, username='user1', password='hola1234')
        board = mixer.blend('catan.Board', name='board_1')
        hexe = mixer.blend('catan.Hexe', token=2, terrain='desert',
                           board=board)
        game_1 = mixer.blend('catan.Game', name="Game1", board=board,
                             robber=hexe)
        player1 = mixer.blend('catan.Player', turn=1, username=user_1,
                              game=game_1, colour="blue")
        building = Building.objects.create(name="settlement", game=game_1,
                                           owner=player1, level=1, index=3)
        assert building.game == game_1
        assert building.owner == player1
        assert building.level == 1
        assert building.index == 3

    def test_building_player(self):
        user_1 = mixer.blend(User, username='user1', password='hola1234')
        board = mixer.blend('catan.Board', name='board_1')
        hexe = mixer.blend('catan.Hexe', token=2, terrain='desert',
                           board=board)
        game1 = mixer.blend('catan.Game', name="Game1", board=board,
                            robber=hexe)
        game2 = mixer.blend('catan.Game', name="Game2", board=board,
                            robber=hexe)
        player1 = Player.objects.create(turn=1, username=user_1,
                                        game=game2, colour="blue")
        building = Building.objects.create(name="settlement", game=game1,
                                           owner=player1, level=1, index=3)
        try:
            building.full_clean()
        except ValidationError as e:
            error = 'Cannot be player of other game'
            assert error in e.message_dict['__all__']

    def test_building_invalid_level(self):
        user_1 = mixer.blend(User, username='user1', password='hola1234')
        board = mixer.blend('catan.Board', name='board_1')
        hexe = mixer.blend('catan.Hexe', token=2, terrain='desert',
                           board=board)
        game_1 = mixer.blend('catan.Game', name="Game1", board=board,
                             robber=hexe)
        player1 = mixer.blend('catan.Player', turn=1, username=user_1,
                              game=game_1, colour="blue")
        building = mixer.blend('catan.Building', name="settlement",
                               game=game_1,
                               owner=player1, level=0, index=6)
        try:
            building.full_clean()
        except ValidationError as e:
            error = 'The index with level 0 must be between 0 and 5.'
            assert error in e.message_dict['__all__']
        building = mixer.blend('catan.Building', name="settlement",
                               game=game_1,
                               owner=player1, level=1, index=18)
        try:
            building.full_clean()
        except ValidationError as e:
            error = 'The index with level 1 must be between 0 and 17.'
            assert error in e.message_dict['__all__']
        building = mixer.blend('catan.Building', name="settlement",
                               game=game_1,
                               owner=player1, level=2, index=30)
        try:
            building.full_clean()
        except ValidationError as e:
            error = 'The index with level 2 must be between 0 and 29.'
            assert error in e.message_dict['__all__']
