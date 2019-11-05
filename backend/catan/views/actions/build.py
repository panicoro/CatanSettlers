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


def checkVertex(level, index):
    rta = False
    vertex = VertexPosition.objects.filter(level=level, index=index)
    if vertex.exists():
        rta = True
        return rta
    return rta


def ResourceBuild(player_id, game_id):
    """
    Return a variable variable size list
    if you find the items.
    """
    list_resource = Resource.objects.filter(owner=player_id, game=game_id)
    brick = True
    lumber = True
    wool = True
    grain = True
    rta = []
    for resource in list_resource:
        if resource.resource_name == "brick" and brick:
            brick = False
            rta.append(resource)
        if resource.resource_name == "lumber" and lumber:
            lumber = False
            rta.append(resource)
        if resource.resource_name == "wool" and wool:
            wool = False
            rta.append(resource)
        if resource.resource_name == "grain" and grain:
            grain = False
            rta.append(resource)
    return rta


def CheckPosition(game_id, level, index):
    rta = True
    position = VertexPosition.objects.filter(level=level,
                                             index=index).get()
    building = Building.objects.filter(game=game_id, position=position)
    if building.exists():
        rta = False
        return rta
    return rta


def CheckRoad(player_id, game_id, level, index):
    """
    Returns True if there is one of the vertices of the player's paths
        matches the VertexPosition entered by it.
    """
    vertex = VertexPosition.objects.filter(level=level, index=index).get()
    rta = False
    road_player = Road.objects.filter(Q(owner=player_id, game=game_id,
                                        vertex_1=vertex) |
                                      Q(owner=player_id, game=game_id,
                                        vertex_2=vertex))
    if road_player.exists():
        rta = True
    return rta


def CheckBuild(game_id, level, index):
    """
    Returns True if there is no construction in the neighbors of the
        VertexPosition entered by the player.
    """
    list_build = Building.objects.filter(game=game_id)
    list_vertex = VertexInfo(level, index)
    rta = True
    for build in list_build:
        for vertex in list_vertex:
            if build.position.level == vertex[0]:
                if build.position.index == vertex[1]:
                    rta = False
                    return rta
    return rta


def deleteResource(list_resource):
    """
    Remove resources from the list.
    """
    for resource in list_resource:
        resource.delete()


def build_settlement(payload, game, player):
    print(payload)
    level = payload['level']
    index = payload['index']
    # Check that the position exists
    if not checkVertex(level, index):
        response = {"detail": "Non-existent position"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    # Check that the position is available
    if not CheckPosition(game.id, level, index):
        response = {"detail": "Busy position"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    necessary_resources = ResourceBuild(player.id, game.id)
    # Check that the pleyer has the necessary resources
    if len(necessary_resources) != 4:
        response = {"detail": "It does not have" +
                    "the necessary resources"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    is_road = CheckRoad(player.id, game.id, level, index)
    is_building = CheckBuild(game.id, level, index)
    # Check that there are no building in the neighboring vertex
    # Checking that the player has a road in the vertex
    if not is_building or not is_road:
        response = {"detail": "Invalid position"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    position = VertexPosition.objects.filter(level=level,
                                             index=index).get()
    new_build = Building(game=game, name='settlement', owner=player,
                         position=position)
    new_build.save()
    point = player.victory_points + 1
    player.victory_points = point
    player.save()
    deleteResource(necessary_resources)
    return Response(status=status.HTTP_200_OK)
