from catan.models import *
import json
import os


MYDIR = os.path.dirname(__file__)


def HexagonInfo(level, index):
    with open('catan/HexaVerVecinos.json') as file:
        data = json.load(file)

        for aux in data['data']:
            hexagon = aux['hexagono']
            if level == hexagon[0] and index == hexagon[1]:
                return aux['vecinos']


def check_player_in_turn(game, player):
    """
    A method to check if the player is in turn in the given game.
    Args:
    @game: a started game.
    @player: a player in the game.
    """
    return game.current_turn.user == player.username
