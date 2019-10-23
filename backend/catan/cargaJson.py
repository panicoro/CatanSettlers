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
