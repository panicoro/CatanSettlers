import pytest
from django.contrib.auth.models import User
from catan.models import Board, Hexe, HexePosition, VertexPosition
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestModels:

    def test_hexe_position(self):
        hexe_position = HexePosition.objects.create(level=1, index=1)
        assert hexe_position.level == 1
        assert hexe_position.index == 1

    def test_board(self):
        board = Board.objects.create(name='Colonos')
        assert board.name == 'Colonos'

    def test_hexe(self):
        board = Board.objects.create(name='Colonos')
        hexe_position = HexePosition.objects.create(level=1, index=1)
        hexe = Hexe.objects.create(terrain='ORE', token=2, board=board,
                                   position=hexe_position)
        assert hexe.board == board
        assert hexe.position == hexe_position

    def test_of_all(self):
        board = Board.objects.create(name='Colonos')
        hexe_position = HexePosition.objects.create(level=1, index=1)
        hexe = Hexe.objects.create(terrain='ORE', token=2, board=board,
                                   position=hexe_position)
        assert board.name == 'Colonos'
        assert hexe_position.level == hexe.position.level
        assert hexe_position.index == hexe.position.index
        assert hexe.position == hexe_position
        assert hexe.terrain == 'ORE'
        assert hexe.token == 2
        assert hexe.board == board

    def test_HexePositionNoValid(self):
        hexe_position = HexePosition.objects.create(level=0, index=1)
        try:
            hexe_position.full_clean()
        except ValidationError as e:
            error = 'The index with level 0 must be between 0 and 0.'
            assert error in e.message_dict['__all__']

        hexe_position = HexePosition.objects.create(level=1, index=6)
        try:
            hexe_position.full_clean()
        except ValidationError as e:
            error = 'The index with level 1 must be between 0 and 5.'
            assert error in e.message_dict['__all__']

        hexe_position = HexePosition.objects.create(level=2, index=12)
        try:
            hexe_position.full_clean()
        except ValidationError as e:
            error = 'The index with level 2 must be between 0 and 11.'
            assert error in e.message_dict['__all__']

    def test_VertexPositionNoValid(self):
        vertex_position = VertexPosition.objects.create(level=0, index=6)
        try:
            vertex_position.full_clean()
        except ValidationError as e:
            error = 'The index with level 0 must be between 0 and 5.'
            assert error in e.message_dict['__all__']

        vertex_position = VertexPosition.objects.create(level=1, index=18)
        try:
            vertex_position.full_clean()
        except ValidationError as e:
            error = 'The index with level 1 must be between 0 and 17.'
            assert error in e.message_dict['__all__']

        vertex_position = VertexPosition.objects.create(level=2, index=30)
        try:
            vertex_position.full_clean()
        except ValidationError as e:
            error = 'The index with level 2 must be between 0 and 29.'
            assert error in e.message_dict['__all__']
