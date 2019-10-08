from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game, Resource, Player
from .serializers import GameSerializer, ResourceSerializer, PlayerSerializer
from django.http import Http404

class ResourceList(APIView):

    def get(self, request, pk): 
        queryset = Resource.objects.all()
        serializer = ResourceSerializer(queryset, many=True)
        return Response(serializer.data)