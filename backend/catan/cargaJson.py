import json


def Hexagono(level,index):
    with open('catan/HexaVerVecinos.json') as file:
        data = json.load(file)

        for aux in data['data']:
            hexagono=aux['hexagono']
            if level== hexagono[0] & index== hexagono[1]:
                return aux['vecinos']


def Vertice(level, index):
    with open('catan/VertexVecinos.json') as file:
        data = json.load(file)

        for aux in data["data"]:
            vertice = aux['vertice']
            if level== vertice[0] and index== vertice[1]:
                return aux['vecinos']

def ResourceBuild(list_resource):
    ladrillo = True
    madera = True
    lana = True 
    cereal = True
    rta = []
    for resource in list_resource:
        if resource.resource_name =="brick" and ladrillo:
            ladrillo = False
            rta.append(resource)
        if resource.resource_name == "lumber" and madera:
            madera = False
            rta.append(resource)
        if resource.resource_name == "wool" and lana:
            lana = False
            rta.append(resource)
        if resource.resource_name == "grain" and cereal:
            cereal = False
            rta.append(resource)

    return rta

def ResourcesRoad(list_resource):
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

def CheckRoads(list_road, level, index):
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

def CheckRoads_Road(list_road, level1, index1, level2, index2):
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

def CheckBuild(list_build, list_vertex, level, index):
    rta = True
    for build in list_build:
        for vertex in list_vertex:
            if build.position.level == vertex[0]:
                if build.position.index == vertex[1]:
                    rta = False
                    return rta
            if build.position.level == level:
                if build.position.index == index:
                    rta = False
                    return rta
    return rta

def CheckBuild_Road(list_build, level1, index1, level2, index2):
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

def CheckPositionRoad(list_all_road,level1,index1,level2,index2):
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

def deleteResource(list_resource):
    for resource in list_resource:
            #Resource.delete(Resource,using=int(resource.id))
            resource.delete()

