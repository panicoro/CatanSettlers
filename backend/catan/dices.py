"""
Module to manage the throw of the dices in the game
"""
from catan.models import *
from random import *
from catan.cargaJson import HexagonInfo
import math


def throw_dice():
    """
    A method to generate a thow of dice
    (uniform discrete distribution).
    """
    return 1 * int(6 * random()) + 1


def set_not_last_gained(owner):
    """
    A method to remove resources as obtained in the last turn.
    Args:
    owner: the player who owns the resources.
    """
    # Get the last gained of the owner
    resources_last_gained = Resource.objects.filter(last_gained=True,
                                                    owner=owner)
    # Set the resources to False in last_gained field
    if len(resources_last_gained) != 0:
        for resource in resources_last_gained:
            resource.last_gained = False
            resource.save()


def set_players_resources_not_last_gained(players):
    """
    A method to set the resources of a list of players
    as not last gained.
    Args:
    players: a list of players.
    """
    for player in players:
        set_not_last_gained(player)


def random_discard(players):
    """
    for player in players:
        if player.resources_cards > 7:
            resources = Resource.objects.filter(owner=player)
            resource_position = []
            for i in range(0, len(resources)):
                resource_position.append(i)
            shuffle(resource_position)
            resource_position = resource_position[0:math.floor(len(resource_position)/2)]
            for elem in resource_position:
                resources[elem].delete()
    """



def gain_resources(game, owner, resource_name, amount):
    """
    A method for players to gain resources.
    Args:
    game: the game in which the owner is.
    owner: a player who will get the resources.
    resource_name: the type of resources to obtain.
    amount: the amount of resources to obtain.
    """
    for i in range(amount):
        Resource.objects.create(owner=owner, game=game,
                                resource_name=resource_name,
                                last_gained=True)


def throw_dices(game, current_turn, board):
    # Throw the dices
    dice1 = throw_dice()
    dice2 = throw_dice()
    # Get the sum of dices
    sum_dices = dice1 + dice2
    # Get the hexes with this token from the board
    hexes = Hexe.objects.filter(board=board, token=sum_dices)
    # Get the players of the games
    players = Player.objects.filter(game=game)
    if sum_dices == 7:
        random_discard(players)
    else:
        set_players_resources_not_last_gained(players)
        if len(hexes) != 0:
            for hexe in hexes:
                hexe_level = hexe.position.level
                hexe_index = hexe.position.index
                hexe_neighbors = HexagonInfo(hexe_level, hexe_index)
                for player in players:
                    # get the buildings of the player
                    buildings = Building.objects.filter(owner=player)
                    if len(buildings) != 0:
                        for building in buildings:
                            building_vertex = [building.position.level,
                                            building.position.index]
                            if building_vertex in hexe_neighbors:
                                if building.name == 'settlement':
                                    gain_resources(owner=player, game=game,
                                                resource_name=hexe.terrain,
                                                amount=1)
                                else:
                                    gain_resources(owner=player, game=game,
                                                resource_name=hexe.terrain,
                                                amount=2)
    current_turn.dices1 = dice1
    current_turn.dices2 = dice2
    current_turn.save()
