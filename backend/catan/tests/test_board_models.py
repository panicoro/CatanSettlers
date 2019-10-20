import pytest
from catan.models import Board, Hexe, HexePosition,Game


@pytest.mark.django_db
class TestModels:

    def test_hexe_position(self):
        hexe_position = HexePosition.objects.create(level=1, index=1)
        assert hexe_position.level == 1
        assert hexe_position.index == 1

    def test_board(self):
        board = Board.objects.create(name='Colonos')
        assert board.name == 'Colonos'

    def test_game(self):
        board = Board.objects.create(name='Colonos')
        game = Game.objects.create(name='Juego 1', board=board)
        assert game.name == 'Juego 1'

    def test_hexe(self):
        board = Board.objects.create(name='Colonos')
        hexe_position = HexePosition.objects.create(level=1, index=1)
        hexe = Hexe.objects.create(terrain='ORE', token=2, board=board, position=hexe_position)
        assert hexe.board == board
        assert hexe.position == hexe_position

    def test_of_all(self):
        board = Board.objects.create(name='Colonos')
        hexe_position = HexePosition.objects.create(level=1, index=1)
        hexe = Hexe.objects.create(terrain='ORE', token=2, board=board, position=hexe_position)
        assert board.name == 'Colonos'
        assert hexe_position.level == hexe.position.level
        assert hexe_position.index == hexe.position.index
        assert hexe.position == hexe_position
        assert hexe.terrain == 'ORE'
        assert hexe.token == 2
        assert hexe.board == board

    def test_of_all_falla_uno(self):
        board = Board.objects.create(name='Colonos')
        hexe_position = HexePosition.objects.create(level=0, index=1)
        hexe = Hexe.objects.create(terrain='ORE', token=3, board=board, position=hexe_position)
        assert board.name == 'Colonos'
        assert hexe_position.level == hexe.position.level
        assert hexe_position.index == hexe.position.index
        assert hexe.position == hexe_position
        assert hexe.terrain == 'ORE'
        assert hexe.token == 3
        assert hexe.board == board

    def test_of_all_falla_dos(self):
        board = Board.objects.create(name='Colonos')
        hexe_position = HexePosition.objects.create(level=1, index=7)
        hexe = Hexe.objects.create(terrain='ORE', token=4, board=board, position=hexe_position)
        assert board.name == 'Colonos'
        assert hexe_position.level == hexe.position.level
        assert hexe_position.index == hexe.position.index
        assert hexe.position == hexe_position
        assert hexe.terrain == 'ORE'
        assert hexe.token == 4
        assert hexe.board == board

    def test_of_all_falla_tres(self):
        board = Board.objects.create(name='Colonos')
        hexe_position = HexePosition.objects.create(level=2, index=13)
        hexe = Hexe.objects.create(terrain='ORE', token=5, board=board, position=hexe_position)
        assert board.name == 'Colonos'
        assert hexe_position.level == hexe.position.level
        assert hexe_position.index == hexe.position.index
        assert hexe.position == hexe_position
        assert hexe.terrain == 'ORE'
        assert hexe.token == 5
        assert hexe.board == board