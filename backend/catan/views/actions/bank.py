from catan.models import *
from rest_framework.response import Response
from rest_framework import status


def check_is_resource(resource):
    resource_type = ['brick', 'lumber', 'wool',
                     'grain', 'ore']
    return resource in resource_type


def bank_trade(payload, game, player):
    gaven = payload['give']
    received = payload['receive']
    if not check_is_resource(gaven) or not check_is_resource(received):
        response = {"detail": "Non-existent resource"}
        return Response(data=response, status=status.HTTP_403_FORBIDDEN)
    if not player.has_necessary_resources('trade_bank', gaven):
        response = {"detail": "It does not have" +
                    " the necessary resources"}
        return Response(data=response, status=status.HTTP_403_FORBIDDEN)
    player.gain_resources(received, 1)
    player.delete_resources('trade_bank', gaven)
    return Response(status=status.HTTP_200_OK)
