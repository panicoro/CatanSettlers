import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from catan.models import Board, Hexe
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestModels:

    def test_board(self):
        board = mixer.blend('catan.Board', name='Colonos')
        assert board.name == 'Colonos'

    def test_hexe(self):
        board = mixer.blend('catan.Board', name='Colonos')
        hexe = mixer.blend('catan.Hexe', terrain='ore', token=8,
                           level=1, index=4, board=board)
        assert hexe.board == board
        assert hexe.terrain == 'ore'
        assert hexe.token == 8
        assert hexe.level == 1
        assert hexe.index == 4

    def test_hexe_position_no_valid(self):
        board = mixer.blend('catan.Board', name='Colonos')
        hexe = mixer.blend('catan.Hexe', terrain='ore', token=8,
                           level=0, index=1, board=board)
        try:
            hexe.full_clean()
        except ValidationError as e:
            error = 'The index with level 0 must be between 0 and 0.'
            assert error in e.message_dict['__all__']
        hexe = mixer.blend('catan.Hexe', terrain='ore', token=8,
                           level=1, index=6, board=board)
        try:
            hexe.full_clean()
        except ValidationError as e:
            error = 'The index with level 1 must be between 0 and 5.'
            assert error in e.message_dict['__all__']

        hexe = mixer.blend('catan.Hexe', terrain='ore', token=8,
                           level=2, index=12, board=board)
        try:
            hexe.full_clean()
        except ValidationError as e:
            error = 'The index with level 2 must be between 0 and 11.'
            assert error in e.message_dict['__all__']


"""
    def test_VertexPositionNoValid(self):
        vertex_position = VertexPosition.objects.create(level=0, index=6)
        try:
            vertex_position.full_clean()
        except ValidationError as e:
            error = 'The index with level 0 must be between 0 and 5.'
            assert error in e.message_dict['__all__']
        vertex_position = VertexPosition.objects.create(level=1, index=20)
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
"""
