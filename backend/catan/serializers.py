from django.contrib.auth.models import User
from rest_framework import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework.reverse import reverse as api_reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.six import text_type


class SignupSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(SignupSerializer, cls).get_token(user)
        return token

    def validate(self, attrs):
        user = authenticate(username=attrs['username'],
                            password=attrs['password'])
        data = {}
        data['username'] = user.username
        data['email'] = user.email
        refresh = self.get_token(user)
        data['token'] = text_type(refresh)
        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)
        return data
