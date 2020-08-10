from catan.models import *
from rest_framework.response import Response
from rest_framework import status


def buy_card(game, player):
    # Check that the pleyer has the necessary resources
    if not player.has_necessary_resources('buy_card'):
        response = {"detail": "It does not have" +
                    " the necessary resources"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    player.select_card()
    player.delete_resources('buy_card')
    # Check if the player won
    if player.is_winner():
        response = {"detail": "YOU WIN!!!"}
        return Response(response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)
