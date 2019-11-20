from catan.models import *


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
    current_turn.robber_moved = False
    current_turn.save()


def change_turn(game):
    """
    A method to change the player in the turn.
    Args:
    @game:a started game.
    """
    players = Player.objects.filter(game=game)
    current_turn = game.current_turn
    next_player = get_next_player(current_turn, players)
    set_new_turn(current_turn, next_player)
