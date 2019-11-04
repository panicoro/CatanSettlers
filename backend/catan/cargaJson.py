from catan.models import *
import json
import os


MYDIR = os.path.dirname(__file__)


def HexagonInfo(level, index):
    with open('catan/HexaVerVecinos.json') as file:
        data = json.load(file)

        for aux in data['data']:
            hexagon = aux['hexagono']
            if level == hexagon[0] and index == hexagon[1]:
                return aux['vecinos']


# get the neighbors of a given vertex
def VertexInfo(level, index):
    with open(os.path.join(MYDIR, 'VertexVecinos.json')) as file:
        data = json.load(file)

        for aux in data["data"]:
            vertex = aux['vertice']
            if level == vertex[0] and index == vertex[1]:
                return aux['vecinos']


# get the necessary resources
def ResourcesRoad(owner_id, game_id):
    list_resource = Resource.objects.filter(owner=owner_id, game=game_id)
    brick = True
    lumber = True
    rta = []

    for resource in list_resource:
        if resource.resource_name == "brick" and brick:
            rta.append(resource)
            brick = False
        if resource.resource_name == "lumber" and lumber:
            rta.append(resource)
            lumber = False

    return rta


# check the existence of a built road
def CheckRoads_Road(owner_id, game_id, level1, index1, level2, index2):
    list_road = Road.objects.filter(owner=owner_id, game=game_id)
    rta = False
    for road in list_road:
        if road.vertex_1.level == level1:
            if road.vertex_1.index == index1:
                rta = True
                return rta
        if road.vertex_2.level == level1:
            if road.vertex_2.index == index1:
                rta = True
                return rta
        if road.vertex_1.level == level2:
            if road.vertex_1.index == index2:
                rta = True
                return rta
        if road.vertex_2.level == level2:
            if road.vertex_2.index == index2:
                rta = True
                return rta
    return rta


# check the existence of a built building
def CheckBuild_Road(owner_id, game_id, level1, index1, level2, index2):
    list_build = Building.objects.filter(owner=owner_id, game=game_id)
    rta = False
    for build in list_build:
        if build.position.level == level1:
            if build.position.index == index1:
                rta = True
                return rta
        if build.position.level == level2:
            if build.position.index == index2:
                rta = True
                return rta
    return rta


# check if the position given for the new road is repeated
def CheckPositionRoad(game_id, level1, index1, level2, index2):
    list_all_road = Road.objects.filter(game=game_id)
    rta = False
    for road in list_all_road:
        if road.vertex_1.level == level1:
            if road.vertex_1.index == index1:
                if road.vertex_2.level == level2:
                    if road.vertex_2.index == index2:
                        rta = True
                        return rta
        if road.vertex_1.level == level2:
            if road.vertex_1.index == index2:
                if road.vertex_2.level == level1:
                    if road.vertex_2.index == index1:
                        rta = True
                        return rta
    return rta


# delete resource
def deleteResource(owner_id, game_id):
    list_resource = Resource.objects.filter(owner=owner_id, game=game_id)
    for resource in list_resource:
        resource.delete()


# check if it's neighbor
def is_neighbor(list_neighbor, level, index):
    vec = False
    for v in list_neighbor:
        if v[0] == level and v[1] == index:
            vec = True
            return vec
    return vec


def check_player_in_turn(game, player):
    """
    A method to check if the player is in turn in the given game.
    Args:
    @game: a started game.
    @player: a player in the game.
    """
    return game.current_turn.user == player.username


# check that the vertices exist within the allowed range
def checkVertexsPositions(level1, index1, level2, index2):
    exist_v = False
    position_1 = VertexPosition.objects.filter(level=level1,
                                               index=index1)
    position_2 = VertexPosition.objects.filter(level=level2,
                                               index=index2)
    if position_1.exists() and position_2.exists():
        exist_v = True
        return exist_v
    return exist_v
