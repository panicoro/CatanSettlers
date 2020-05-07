from catan.models import *
from rest_framework.response import Response
from rest_framework import status


def change_turn(game):
    """
    A method to change the player in the turn.
    Args:
    @game: a started game.
    """
    if not game.can_change_turn():
        data = {"detail": "must built your first constructions"}
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    game.change_turn()
    return Response(status=status.HTTP_204_NO_CONTENT)
