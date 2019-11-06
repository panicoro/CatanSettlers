from catan.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt import authentication
from django.http import Http404
from random import random
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catan.cargaJson import *
from catan.dices import throw_dices
from rest_framework.permissions import AllowAny
from random import shuffle
from django.db.models import Q
from random import randint


def checkResource(game_id, player_id):
    ore = Q(owner=player_id, game=game_id, resource_name='ore')
    wool = Q(owner=player_id, game=game_id, resource_name='wool')
    grain = Q(owner=player_id, game=game_id, resource_name='grain')
    list_resource = Resource.objects.filter(ore | wool | grain)
    return list_resource


def selectCard(game, player):
    card_type = ['road_building',
                 'year_of_plenty',
                 'monopoly',
                 'victory_point',
                 'knight']
    card_name = card_type[randint(0, 4)]
    new_card = Card(owner=player, game=game, card_name=card_name)
    new_card.save()


def deleteResource(list_resource):
    """
    Remove resources from the list.
    """
    for resource in list_resource:
        resource.delete()


def buy_card(game, player):
    necessary_resources = checkResource(player.id, game.id)
    # Check that the pleyer has the necessary resources
    if len(necessary_resources) != 3:
        response = {"detail": "It does not have" +
                    " the necessary resources"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    selectCard(game, player)
    deleteResource(necessary_resources)
    return Response(status=status.HTTP_200_OK)
