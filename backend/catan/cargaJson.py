import json

def Hexagono(level,index):
    with open('HexaVerVecinos.json') as file:
        data = json.load(file)

        for aux in data['data']:
            hexagono=aux['hexagono']
            if level== hexagono[0] & index== hexagono[1]:
                return aux['vecinos']


def Vertice(level, index):
    with open('VertexVecinos.json') as file:
        data = json.load(file)

        for aux in data["hexagonosVecinos"]:
            vertice = aux['vertice']
            if level== vertice[0] and index== vertice[1]:
                return aux['vecinos']



    