from .models import Resource
from rest_framework import serializers

class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ('id','name')