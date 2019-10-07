from rest_framework import generics
from .models import Game, Resource
from .serializers import GameSerializer,    ResourceSerializer
from django.shortcuts import get_object_or_404

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_object(self, request, *args, **kwargs) :
        print(request.user)
        queryset = self.queryset()
        obj = get_object_or_404(
            queryset
        )

        return obj

class ResourceList(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_object(self) :
        print(request.user)
        print("Hola")
        queryset = self.queryset()
        obj = get_object_or_404(
            queryset
        )

        return obj