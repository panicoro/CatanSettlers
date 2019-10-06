from rest_framework import status
from rest_framework.decorators import api_view  #p/ trabajar las vistas basadas en funciones
from rest_framework.response import Response
from catan.models import Tablero, Hexagono  #importo mis modelos
from catan.serializers import TableroSerializer, HexagonoSerializer

@api_view(['GET', 'POST'])
def lista_tablero(request, format=None):

    if request.method == 'GET':
	    tableros = Tablero.objects.all()		#obtengo todos los tableros
	    serializer = TableroSerializer(tableros, many=True)
	    return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TableroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def lista_hexagono(request, format=None):

    if request.method == 'GET':
	    hexagonos = Hexagono.objects.all()		#obtengo todos los hexagonos
	    serializer = HexagonoSerializer(hexagonos, many=True)
	    return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HexagonoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
