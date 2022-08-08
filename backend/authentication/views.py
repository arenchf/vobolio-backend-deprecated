from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminOrSelf
from .models import CustomUser, Role
from .serializers import ChangePasswordSerializer, MyTokenObtainPairSerializer, CustomUserSerializer, RoleSerializer
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


class UserView(APIView):

    permission_classes = (IsAdminOrSelf,)

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs["user_id"])
        serializer = CustomUserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # print(request.user.id)
        # print(kwargs["user_id"])
        user = CustomUser.objects.get(id=kwargs["user_id"])
        self.check_object_permissions(self.request, user)
        print(user)

        serializer = CustomUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

        # if serializer.is_valid():
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
        # return Response(status=status.HTTP_404_NOT_FOUND)


class RoleView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = RoleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRoleView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs["user_id"])
        serializer = RoleSerializer(user.roles, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = RoleSerializer(data=data)
        if serializer.is_valid():

            role = Role.objects.filter(name=serializer.data["name"])
            if role.exists():
                request.user.roles.add(role.first())
                request.user.save()
                user_serializer = CustomUserSerializer(request.user)
                return Response(user_serializer.data, status.HTTP_202_ACCEPTED)

            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = (IsAdminOrSelf,)

    def put(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs["user_id"])
        self.check_object_permissions(self.request, user)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data["old_password"]):
                raise serializers.ValidationError(
                    {"old_password": "Old password is not correct"})

            user.set_password(serializer.validated_data["new_password"])
            user.save()
            user_serializer = CustomUserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
