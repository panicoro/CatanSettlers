from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt import authentication

class AuthAPIView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        data = request.data
        response={"detail":"Invalid credentials"}

        try:
            data['username'] = data['user']
            data['password'] = data['pass']
        except:
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = authenticate(username=data['username'], password=data['password'])
        except:
            user = None

        if (user != None):
            serializer = self.get_serializer(data=request.data)
            response = serializer.validate(request.data)
        else:
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        return Response(response, status=status.HTTP_201_CREATED)