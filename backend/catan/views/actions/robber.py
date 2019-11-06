from catan.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt import authentication
from django.http import Http404
from random import random, randint
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catan.cargaJson import *
from catan.dices import throw_dices
from rest_framework.permissions import AllowAny
from random import shuffle
from django.db.models import Q


def checkPosition(level, index):
    rta = False
    hexe = HexePosition.objects.filter(level=level, index=index)
    if hexe.exists():
        rta = True
        return rta
    return rta


def move_robber(payload, game, my_user, my_player):
    dice1 = Current_Turn.objects.filter(game=game)[0].dices1
    dice2 = Current_Turn.objects.filter(game=game)[0].dices2

    sum_dices = dice1 + dice2

    if sum_dices == 7:

        level = payload['position']['level']
        index = payload['position']['index']
        player_robber = payload['player']

        if checkPosition(level, index) is False:
            response = {"detail": "There is no hexagon in that position"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        position = HexePosition.objects.filter(level=level,
                                               index=index).get()
        game.robber = position
        game.save()

        buildings = Building.objects.filter(game=game)
        vertex_in_hex = HexagonInfo(level, index)
        buildings_in_hex = []

        for pos in range(0, 6):
            vertex = VertexPosition.objects.filter(
                level=vertex_in_hex[pos][0],
                index=vertex_in_hex[pos][1])[0]
            if Building.objects.filter(position=vertex).exists():
                building = Building.objects.filter(position=vertex)
                buildings_in_hex.append(building)

        owners = []

        for pos in range(len(buildings_in_hex)):
            owners.append(buildings_in_hex[pos][0].owner)

        # If there is no construction in the thief's hexagon #

        if len(owners) == 0:
            response = {
                "detail": "there are no buildings in the hexagon"}
            stat = status.HTTP_204_NO_CONTENT
            return Response(response, stat)

        # If there is only one construction in the thief's hexagon #

        elif len(owners) == 1:
            if str(owners[0].username) in str(my_user):
                response = {
                    "detail": "there are no enemy buildings in the hexagon"}
                stat = status.HTTP_204_NO_CONTENT
                return Response(response, stat)

            resources_list = Resource.objects.filter(owner=owners[0])

            if resources_list.exists():
                resource_robber = Resource.objects.filter(
                    owner=owners[0])[randint(0, len(resources_list)-1)]

                resource_robber.owner = my_player
                resource_robber.last_gained = True
                resource_robber.save()
                response = {"detail": "you stole the resource " +
                            str(resource_robber)}
                stat = status.HTTP_204_NO_CONTENT
                return Response(response, stat)
            response = {"detail": "the player has no resources"}
            stat = status.HTTP_204_NO_CONTENT
            return Response(response, stat)

        # If there is more than one construction in the thief's hexagon #

        else:
            if player_robber is not None:
                if player_robber in str(my_user):
                    response = {"detail": "you can't choose yourself"}
                    stat = status.HTTP_403_FORBIDDEN
                    return Response(response, stat)

                for pos in range(0, len(owners)):
                    if player_robber in str(owners[pos].username):
                        resources_list = Resource.objects.filter(
                            owner=owners[pos])
                        if resources_list.exists():
                            resource_robber = Resource.objects.filter(
                                owner=owners[pos])[randint(
                                    0, len(resources_list)-1)]
                            resource_robber.owner = my_player
                            resource_robber.last_gained = True
                            resource_robber.save()
                            response = {
                                "detail": "you stole the resource " +
                                str(resource_robber)}
                            stat = status.HTTP_204_NO_CONTENT
                            return Response(response, stat)
                        response = {
                            "detail": "the player has no resources"}
                        stat = status.HTTP_204_NO_CONTENT
                        return Response(response, stat)
            response = {
                "detail": "you have to choose a player that has buildings"}
            stat = status.HTTP_403_FORBIDDEN
            return Response(response, stat)

    response = {"detail": "the dices don't give 7"}
    return Response(response, status=status.HTTP_403_FORBIDDEN)
