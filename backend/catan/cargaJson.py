import json


def HexagonInfo(level,index):
    with open('catan/HexaVerVecinos.json') as file:
        data = json.load(file)

        for aux in data['data']:
            hexagon=aux['hexagono']
            if level== hexagon[0] and index== hexagon[1]:
                return aux['vecinos']


def VertexInfo(level, index):
    with open('catan/VertexVecinos.json') as file:
        data = json.load(file)

        for aux in data["data"]:
            vertex = aux['vertice']
            if level== vertex[0] and index== vertex[1]:
                return aux['vecinos']

def ResourceBuild(list_resource):
    birck = True
    lumber = True
    wool = True 
    grain = True
    rta = []
    for resource in list_resource:
        if resource.resource_name =="brick" and birck:
            birck = False
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


def CheckRoad(list_road, level, index):
    rta = False
    for road in list_road:
        if road.vertex_1.level == level:
            if road.vertex_1.index == index:
                rta = True
                return rta
        if road.vertex_2.level == level:
            if road.vertex_2.index == index:
                rta = True
                return rta
    return rta

def CheckBuild(list_build, list_vertex, level, index):
    rta = True
    for build in list_build:
        for vertex in list_vertex:
            if build.position.level == vertex[0]:
                if build.position.index == vertex[1]:
                    rta = False    
                    return rta
            if  build.position.level == level:
                if build.position.index == index:
                    rta = False
                    return rta
    return rta

def deleteResource(list_resource):
    for resource in list_resource:
            resource.delete()

