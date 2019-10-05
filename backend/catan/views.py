from rest_framework import generics
from .models import Resource
from .serializers import ResourceSerializer
from django.shortcuts import get_object_or_404

class ResourceList(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_object(self) :
        queryset = self.queryset()
        obj = get_object_or_404(
            queryset,
            pk=self.kwargs['pk']
        )

        return obj


