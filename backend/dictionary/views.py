
from xmlrpc.client import ResponseError
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dictionary
from .serializers import DetailedDictionarySerializer, DictionarySerializer


class DictionaryView(APIView):

    def get(self, request, *args, **kwargs):
        dictionaries = Dictionary.objects.filter(
            is_visible=True, author=kwargs["user_id"])
        # if not dictionaries:
        #     return Response({"msg": "test"}, status.HTTP_404_NOT_FOUND)
        serializer = DetailedDictionarySerializer(dictionaries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data

        data['author'] = kwargs["user_id"]

        serializer = DictionarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DictionaryDetailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            dictionary = Dictionary.objects.get(id=kwargs['pk'])
        except Dictionary.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DictionarySerializer(dictionary, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        try:
            dictionary = Dictionary.objects.get(id=kwargs['pk'])
        except Dictionary.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['author'] = request.user.id
        serializer = DictionarySerializer(dictionary, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            Dictionary.objects.get(id=kwargs['pk']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Dictionary.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
