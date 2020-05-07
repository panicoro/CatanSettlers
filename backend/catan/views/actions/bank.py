from catan.models import *
from rest_framework.response import Response
from rest_framework import status


def check_is_resource(give, receive):
    resource_type = ['brick', 'lumber', 'wool',
                     'grain', 'ore']
    return give in resource_type and receive in resource_type


def bank_trade(payload, game, player):
    give = payload['give']
    receive = payload['receive']
    if not check_is_resource(give, receive):
        response = {"detail": "Non-existent resource"}
        return Response(data=response, status=status.HTTP_403_FORBIDDEN)
    if not player.has_necessary_resources('trade_bank', give):
        response = {"detail": "It does not have" +
                    " the necessary resources"}
        return Response(data=response, status=status.HTTP_403_FORBIDDEN)
    player.gain_resources(receive, 1)
    player.delete_resources('trade_bank', give)
    return Response(status=status.HTTP_200_OK)
