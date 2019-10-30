import json
import os


MYDIR = os.path.dirname(__file__)


def HexagonInfo(level, index):
    with open(os.path.join(MYDIR, 'HexaVerVecinos.json')) as file:
        data = json.load(file)

        for aux in data['data']:
            hexagon = aux['hexagono']
            if level == hexagon[0] and index == hexagon[1]:
                return aux['vecinos']


def VertexInfo(level, index):
    with open(os.path.join(MYDIR, 'VertexVecinos.json')) as file:
        data = json.load(file)

        for aux in data["data"]:
            vertex = aux['vertice']
            if level == vertex[0] and index == vertex[1]:
                return aux['vecinos']
