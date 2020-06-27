from catan.models import *
from rest_framework.response import Response
from rest_framework import status
from catan.views.actions.bank import check_is_resource


def play_monopoly_card(resource, game, player):
    if not player.has_card('monopoly'):
        response = {"detail": 'You have not monopoly card'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    if not check_is_resource(resource):
        response = {"detail": "Non-existent resource"}
        return Response(data=response, status=status.HTTP_403_FORBIDDEN)
    players = Player.objects.filter(game=game)
    for player_to_steal in players:
        count = player_to_steal.delete_resources('monopoly', resource)
        if count != 0:
            player.gain_resources(resource, count)
    return Response(status=status.HTTP_200_OK)