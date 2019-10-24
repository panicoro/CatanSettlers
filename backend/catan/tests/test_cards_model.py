import pytest
from catan.models import *
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:
    def test_card(self):
        hexe_position = HexePosition.objects.create(level=1, index=2)

        board = Board.objects.create(name='Colonos')

        game = Game.objects.create(name='Juego', board=board,
                                   robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        card = mixer.blend(Card, owner=player1,
                           game=game, card_name='monopoly')
        resource = mixer.blend(Resource, resource_name='wool',
                               game=game, owner=player1)
        assert card.card_name == 'monopoly'
        assert resource.resource_name == 'wool'
        assert card.owner == player1
        assert player1.username == user1

    def test__str__(self):
        hexe_position = HexePosition.objects.create(level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game = Game.objects.create(name='Juego', board=board,
                                   robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game, colour='Rojo',
                              development_cards=1, resources_cards=2)
        assert str(player1) == str(player1.username)
        card = mixer.blend(Card, owner=player1,
                           game=game, card_name='monopoly')
        assert str(card) == card.card_name
        resource = mixer.blend(Resource, resource_name='wool', owner=player1)
        assert str(resource) == resource.resource_name

    def test_Not_valid_Card(self):
        hexe_position = HexePosition.objects.create(level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        game2 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        card = mixer.blend(Card, owner=player1,
                           game=game2, card_name='monopoly')
        try:
            card.full_clean()
        except ValidationError as e:
            error = 'Cannot be player of other game'
            assert error in e.message_dict['__all__']

    def test_Not_valid_Resource(self):
        hexe_position = HexePosition.objects.create(level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        game2 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        resource = mixer.blend(Resource, owner=player1,
                               game=game2, resource_name='wool')
        try:
            resource.full_clean()
        except ValidationError as e:
            error = 'Cannot be player of other game'
            assert error in e.message_dict['__all__']

    def test_Not_valid_Building(self):
        hexe_position = HexePosition.objects.create(level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        game2 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
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

    def test_Not_valid_Road(self):
        hexe_position = HexePosition.objects.create(level=1, index=2)
        board = Board.objects.create(name='Colonos')
        game1 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        game2 = Game.objects.create(name='Juego', board=board,
                                    robber=hexe_position)
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1,
                              game=game1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        vertex1 = VertexPosition.objects.create(level=1, index=2)
        vertex2 = VertexPosition.objects.create(level=1, index=1)
        road = mixer.blend(Road, owner=player1,
                           game=game2, vertex_1=vertex1, vertex_2=vertex2)
        try:
            road.full_clean()
        except ValidationError as e:
            error = 'Cannot be player of other game'
            assert error in e.message_dict['__all__']
