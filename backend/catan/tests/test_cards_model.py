import pytest
from catan.models import *
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:
    def test_card(self):
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        card = mixer.blend(Card, player=player1, card_name='monopoly')
        resource = mixer.blend(Resource, resource_name='wool', owner=player1)
        assert card.card_name == 'monopoly'
        assert resource.resource_name == 'wool'
        assert card.player == player1
        assert player1.username == user1

    def test__str__(self):
        user1 = mixer.blend(User, username='Nico', password='minombrenico')
        player1 = mixer.blend(Player, username=user1, colour='Rojo',
                              development_cards=1, resources_cards=2)
        assert str(player1) == str(player1.username)
        card = mixer.blend(Card, player=player1, card_name='monopoly')
        assert str(card) == card.card_name
        resource = mixer.blend(Resource, resource_name='wool', owner=player1)
        assert str(resource) == resource.resource_name
        vertex_settlements = mixer.blend(Vertex_position_settlements,
                                         player=player1, level=1, index=2)
        assert str(vertex_settlements) == str(vertex_settlements)
        vertex_cities = mixer.blend(Vertex_position_cities,
                                    player=player1, level=2, index=3)
        assert str(vertex_cities) == str(vertex_cities)
        road_pos = mixer.blend(Road_position, player=player1, level1=1,
                               index1=2, level2=4, index2=6)
        assert str(road_pos) == str(road_pos)
        last_gained = mixer.blend(Last_gained, player=player1,
                                  resources=resource)
        assert str(last_gained) == last_gained.resources.resource_name
