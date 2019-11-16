from catan.models import *
from rest_framework.response import Response
from rest_framework import status


def get_next_player(current_turn, players):
    """
    A method to get the next player in the turn of a
    started game.
    Args:
    @current_turn: a Current_Turn object of a started game.
    @players: a queryset of the players of a started game.
    """
    player_in_turn = players.filter(username=current_turn.user).get()
    # Get the number of the actual turn
    actual_turn = player_in_turn.turn
    # Calculate the next turn in the game...
    # In the stage 'FIRST_CONSTRUCTION' and 'FULL_PLAY' the order
    # is the natural, and in the stage 'SECOND_CONSTRUCTION' the order
    # is the inverse
    game_stage = current_turn.game_stage
    if game_stage == 'first_construction':
        if actual_turn != 4:
            next_turn = actual_turn + 1
        else:
            next_turn = actual_turn
            current_turn.game_stage = 'second_construction'
            current_turn.save()
    elif game_stage == 'second_construction':
        if actual_turn != 1:
            next_turn = actual_turn - 1
        else:
            next_turn = actual_turn
            current_turn.game_stage = 'full_play'
            current_turn.save()
    else:
        if actual_turn == 4:
            next_turn = 1
        else:
            next_turn = actual_turn + 1
    # Get the player with the next turn
    next_player = players.filter(turn=next_turn).get()
    return next_player


def set_new_turn(current_turn, player):
    """
    A method to set a new player in turn on a given
    current turn of a started game.
    Args:
    @current_turn: a Current_Turn object of a started game.
    @ player: a player to set as new in the turn.
    """
    current_turn.user = player.username
    current_turn.last_action = 'non_blocking_action'
    current_turn.save()


def change_turn(game):
    """
    A method to change the player in the turn.
    Args:
    @game: a started game.
    """
    players = Player.objects.filter(game=game)
    game_stage = game.current_turn.game_stage
    last_action = game.current_turn.last_action
    if game_stage != 'full_play':
        if last_action != 'build_road':
            data = {"detail": "must built your first constructions"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
    next_player = get_next_player(game.current_turn, players)
    set_new_turn(game.current_turn, next_player)
    return Response(status=status.HTTP_204_NO_CONTENT)
