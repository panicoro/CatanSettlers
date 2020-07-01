from catan.models import *
from rest_framework.response import Response
from rest_framework import status
from catan.views.actions.bank import check_is_resource


def play_year_of_plenty(resources, game, player):
    if not player.has_card('year_of_plenty'):
        response = {"detail": 'You have not year of plenty card'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    for res in resources:
        if not check_is_resource(res):
            response = {"detail": "Non-existent resource"}
            return Response(data=response, status=status.HTTP_403_FORBIDDEN)
    player.gain_resources(resources[0], 1)
    player.gain_resources(resources[1], 1)
    return Response(status=status.HTTP_200_OK)
