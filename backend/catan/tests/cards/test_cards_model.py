import pytest
from catan.models import *
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:
    def test_card(self):
        hexe = mixer.blend('catan.Hexe', level=1, index=2,
                           terrain='ore', token=6)
        board = mixer.blend('catan.Board', name='Colonos')
        game = mixer.blend('catan.Game', name='Juego', board=board,
                           robber=hexe)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend('catan.Player', username=user1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        card = mixer.blend(Card, owner=player1,
                           game=game, name='monopoly')
        assert card.name == 'monopoly'
        assert card.owner == player1
        assert card.game == game
        assert player1.username == user1

    def test_not_valid_card(self):
        hexe = mixer.blend('catan.Hexe', level=1, index=2,
                           terrain='ore', token=6)
        board = mixer.blend('catan.Board', name='Colonos')
        game1 = mixer.blend('catan.Game', name='Juego', board=board,
                            robber=hexe)
        game2 = Game.objects.create(name='Juego2', board=board,
                                    robber=hexe)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        card = mixer.blend(Card, owner=player1,
                           game=game2, name='monopoly')
        try:
            card.full_clean()
        except ValidationError as e:
            error = 'Cannot be player of other game'
            assert error in e.message_dict['__all__']

    def test_not_valid_building(self):
        hexe = mixer.blend('catan.Hexe', level=1, index=2,
                           terrain='ore', token=6)
        board = mixer.blend('catan.Board', name='Colonos')
        game1 = mixer.blend('catan.Game', name='Juego', board=board,
                            robber=hexe)
        game2 = Game.objects.create(name='Juego2', board=board,
                                    robber=hexe)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        building = mixer.blend(Building, owner=player1,
                               game=game2, name='city')
        try:
            building.full_clean()
        except ValidationError as e:
            error = 'Cannot be player of other game'
            assert error in e.message_dict['__all__']

    def test_not_valid_road(self):
        hexe = mixer.blend('catan.Hexe', level=1, index=2,
                           terrain='ore', token=6)
        board = mixer.blend('catan.Board', name='Colonos')
        game1 = mixer.blend('catan.Game', name='Juego', board=board,
                            robber=hexe)
        game2 = Game.objects.create(name='Juego2', board=board,
                                    robber=hexe)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        road = mixer.blend(Road, owner=player1,
                           game=game2, level_1=1, index_1=2,
                           level_2=1, index_2=1)
        try:
            road.full_clean()
        except ValidationError as e:
            error = 'Cannot be player of other game'
            assert error in e.message_dict['__all__']
