from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer
from rest_framework import serializers


class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():

            email_exists = CustomUser.objects.filter(
                email=serializer.validated_data["email"]).exists()
            username_exists = CustomUser.objects.filter(
                username=serializer.validated_data["username"]).exists()
            if email_exists and username_exists:
                return Response({"email": "Email already exists", "username": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if email_exists:
                return Response({"email": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if username_exists:
                return Response({"username": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
