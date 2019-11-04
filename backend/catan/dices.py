"""
Module to manage the throw of the dices in the game
and the distribution of resources after the throw.
Also has the logic to discart cards when the sum is equal to 7.
"""
from catan.models import *
from random import random
from catan.cargaJson import HexagonInfo


def throw_dice():
    """
    A function to generate a thow of dice
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
    owner.resources_cards += amount
    owner.save()


def throw_twoDices(dice1=0, dice2=0):
    """
    A function to get the throw of two dices
    Params:
    @dice1: the value of the dice1 (used only for testing).
    @dice2: the value of the dice2 (used only for testing).
    """
    if (dice1 == 0) and (dice2 == 0):
        dice1 = throw_dice()
        dice2 = throw_dice()
        return (dice1, dice2)
    else:
        return (dice1, dice2)


def distribute_resources(hexes, players, game):
    """
    A method that takes a list of hexagons and a list of players.
    For each hex on the list, check if each player on the list has
    buildings at the vertices of that hex; if the player has them
    increases his amount of resources.
    Params:
    @hexes: a list of selected objects Hexes of the board.
    @players: a list of players of a started game.
    @game: a started game.
    """
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


def throw_dices(game, dice1=0, dice2=0):
    """
    A method that rolls the two dice at the beginning of the turn and
    distributes the resources according to the hexagons with the
    token of the sum of the dice.
    Params:
    @game: a started game.
    @dice1: the value of the dice1 (used only for testing).
    @dice2: the value of the dice2 (used only for testing).
    """
    # Get the trow of dices and then sum them.
    two_dices = throw_twoDices(dice1, dice2)
    sum_dices = sum(two_dices)
    # Get the players of the games
    players = Player.objects.filter(game=game)
    # if sum_dices == 7:
    #   random_discart(players)
    # else (poner lo que sigue en else hasta inclusive distribute_resources):
    set_players_resources_not_last_gained(players)
    # Get the hexes with this token from the board
    hexes = Hexe.objects.filter(board=game.board, token=sum_dices)
    # If the robber is in one hexes with the token of the sum
    # then we must exclude it...
    if hexes.filter(position=game.robber).exists():
        hexes = hexes.exclude(position=game.robber)
    # Then distribute_resources...
    distribute_resources(hexes, players, game)
    game.current_turn.dices1 = two_dices[0]
    game.current_turn.dices2 = two_dices[1]
    game.current_turn.save()
