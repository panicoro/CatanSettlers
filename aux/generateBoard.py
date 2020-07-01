"""
Random Board Generator
"""
from catan.models import Hexe, Board, generateHexesPositions
from random import randint, choice, shuffle

TYPE_RESOURCE = ['brick', 'wool', 'grain', 'ore', 'lumber']
BOARD = ['wool'] * 4 + ['brick'] * 3 + ['grain'] * 4 + \
        ['ore'] * 3 + ['lumber'] * 4

def generateTokens():
    tokens = []
    for i in range(3, 12):
        for k in range(2):
            tokens.append(i)
    tokens.append(2)
    tokens.append(12)
    return tokens

def generateBoard(name):
    """
    A method to generate a random board (with one desert).
    Args:
    name: name of the board to create.
    """
    new_board = Board(name=name)
    new_board.save()
    hexes_positions = generateHexesPositions()
    # Choise one hexe_position for desert...
    position_for_desert = randint(0, 18)
    hexe_position_desert = hexes_positions[position_for_desert]
    hexes_positions.remove(hexe_position_desert)
    hexe_desert = Hexe(board=new_board, terrain='desert',
                       level=hexe_position_desert[0],
                       index=hexe_position_desert[1])
    hexe_desert.save()
    shuffle(BOARD)
    TOKENS = generateTokens()
    shuffle(TOKENS)
    for token, hexe_pos, terrain in zip(TOKENS, hexes_positions, BOARD):
        new_hexe = Hexe(board=new_board, token=token,
                        terrain=terrain,
                        level=hexe_pos[0],
                        index=hexe_pos[1])
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
    hexes_positions = [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4],
                       [1, 5], [2, 0], [2, 1], [2, 2]]
    tokens = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
    terrain_types = TYPE_RESOURCE + TYPE_RESOURCE
    for i in range(0, len(hexes_positions)):
        new_terrain = terrain_types[i]
        new_token = tokens[i]
        new_hexe = Hexe(board=new_board, token=new_token,
                        terrain=new_terrain, level=hexes_positions[i][0],
                        index=hexes_positions[i][1])
        new_hexe.save()
    return new_board
