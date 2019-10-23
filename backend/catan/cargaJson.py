import json


def Hexagono(level,index):
    with open('catan/HexaVerVecinos.json') as file:
        data = json.load(file)

        for aux in data['data']:
            hexagono=aux['hexagono']
            if level== hexagono[0] and index== hexagono[1]:
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
            #Resource.delete(Resource,using=int(resource.id))
            resource.delete()

