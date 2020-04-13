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
    list_resource = Resource.objects.filter(owner=player_id, game=game_id)
    ore = True
    wool = True
    grain = True
    rta = []
    for resource in list_resource:
        if resource.resource_name == "ore" and ore:
            rta.append(resource)
            ore = False
        if resource.resource_name == "wool" and wool:
            rta.append(resource)
            wool = False
        if resource.resource_name == "grain" and grain:
            rta.append(resource)
            grain = False
    return rta


def canBuyCard(game, player):
    list_resource = checkResource(game, player)
    return len(list_resource) == 3


def checkWinner(game, player):
    winner = False
    points = player.victory_points
    card_vic_points = Card.objects.filter(
        game=game, owner=player,
        card_name='victory_point').count()
    suma_total = points + card_vic_points

    if suma_total >= 10:
        winner = True
        user = User.objects.get(username=player.username)
        game.winner = user
        game.save()
    return winner


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
    necessary_resources = checkResource(game.id, player.id)
    # Check that the pleyer has the necessary resources
    if len(necessary_resources) != 3:
        response = {"detail": "It does not have" +
                    " the necessary resources"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    selectCard(game, player)
    deleteResource(necessary_resources)
    # Check if the player won
    if checkWinner(game, player):
        response = {"detail": "GANASTE"}
        return Response(response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)
