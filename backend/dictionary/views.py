
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dictionary
from .serializers import DictionarySerializer



class DictionaryView(APIView):

    def get(self,request):
        dictionaries = Dictionary.objects.filter(is_visible=True)
        serializer = DictionarySerializer(dictionaries,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        data = request.data
        print(request.user)
        data['author'] = request.user.id
        serializer = DictionarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    

