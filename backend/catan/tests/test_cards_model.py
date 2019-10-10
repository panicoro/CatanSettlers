import pytest
from catan.models import Card, Player
from django.contrib.auth.models import User



@pytest.mark.django_db
class TestModels:
    def test_name(self):
        user1 = User.objects.create(username = 'Nico', password = 'minombrenico')
        player1 = Player.objects.create(username = user1, colour = 'Rojo', development_cards = 1, resources_cards = 2)
        card = Card.objects.create(player = player1, name = 'monopoly')
        assert card.name == 'monopoly'
        assert card.player == player1
        assert player1.username == user1
