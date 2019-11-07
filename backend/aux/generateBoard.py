"""
Random Board Generator
"""
from catan.models import (Hexe, HexePosition, Board,
                          VertexPosition)
from random import randint, choice

TYPE_RESOURCE = ['brick', 'wool', 'grain', 'ore', 'lumber']


def generateHexesPositions():
    """
    A method to generate all the positions of the hexagons in the board:
    Generate only one time.
    """
    top_ranges = [1, 6, 12]
    for i in range(0, 3):
        for j in range(0, top_ranges[i]):
            new_hexe_position = HexePosition(level=i, index=j)
            new_hexe_position.save()


def generateVertexPositions():
    """
    A method to generate all the positions of the vertex in the board:
    Generate only one time.
    """
    top_ranges = [6, 18, 30]
    for i in range(0, 3):
        for j in range(0, top_ranges[i]):
            new_vertex_position = VertexPosition(level=i, index=j)
            new_vertex_position.save()


def generateBoard(name):
    """
    A method to generate a random board (with one desert).
    Args:
    name: name of the board to create.
    """
    new_board = Board(name=name)
    new_board.save()
    hexes_positions = HexePosition.objects.all()
    # Choise one hexe_position for desert...
    position_for_desert = randint(0, 18)
    hexe_position_desert = hexes_positions[position_for_desert]
    hexes_positions = hexes_positions.exclude(id=(position_for_desert + 1))
    hexe_desert = Hexe(board=new_board, terrain='desert',
                       position=hexe_position_desert)
    hexe_desert.save()
    for i in range(0, len(hexes_positions)-1):
        new_terrain = TYPE_RESOURCE[randint(0, 4)]
        new_token = choice([i for i in range(2, 12) if i not in [7]])
        new_hexe = Hexe(board=new_board, token=new_token,
                        terrain=new_terrain, position=hexes_positions[i])
        new_hexe.save()
    return new_board


def generateBoardTest():
    """
    A method to generate a board for test the throw of
    two dices. This board has only 10 hexes with the following
    tokens...
    * tokens and their resources types:
    2 => 'brick'
    3 => 'wool'
    4 => 'grain'
    5 => 'ore'
    6 => 'lumber'
    8 => 'brick'
    9 => 'wool'
    10 => 'grain'
    11 => 'ore'
    12 => 'lumber'
    """
    new_board = Board(name="test_board")
    new_board.save()
    hexes_positions = HexePosition.objects.all()[:10]
    tokens = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
    terrain_types = TYPE_RESOURCE + TYPE_RESOURCE
    for i in range(0, len(hexes_positions)):
        new_terrain = terrain_types[i]
        new_token = tokens[i]
        new_hexe = Hexe(board=new_board, token=new_token,
                        terrain=new_terrain, position=hexes_positions[i])
        new_hexe.save()
    return new_board
