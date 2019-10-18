import pytest
from catan.models import Board, Hexes, VertexPosition

@pytest.mark.django_db
class TestModels:
    def test_name(self):
        board = Board.objects.create(name = 'Colonos')
        hexe = Hexes.objects.create(terrain = 'ORE', token = 2, board = board)
        assert board.name == 'Colonos'
        assert hexe.terrain == 'ORE'
        assert hexe.token == 2
        assert hexe.board == board