
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.decorators import api_view

from .models import Category, Word
from dictionary.models import Dictionary
from .serializers import CategorySerializer, TrainingSerializer, WordSerializer

import random


class CategoryView(APIView):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(
            is_visible=True, dictionary=kwargs["pk"])
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.id
        data['dictionary'] = kwargs["pk"]
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            category = Category.objects.get(
                is_visible=True, dictionary=kwargs['pk'], id=kwargs['category_id'])
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        try:
            category = Category.objects.get(
                is_visible=True, dictionary=kwargs['pk'], id=kwargs['category_id'])
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['author'] = request.user.id
        data['dictionary'] = kwargs["pk"]
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            Category.objects.get(
                is_visible=True, dictionary=kwargs['pk'], id=kwargs['category_id']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class WordView(APIView):
    def get(self, request, *args, **kwargs):
        print("GETTING", request)
        category = request.GET.get('category', None)
        if category:
            words = Word.objects.filter(
                is_visible=True, dictionary=kwargs["pk"], category=category).order_by('-id')
        else:
            words = Word.objects.filter(
                is_visible=True, dictionary=kwargs["pk"]).order_by('-id')

        paginator = LimitOffsetPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(words, request)
        serializer = WordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.id
        data['dictionary'] = kwargs["pk"]
        serializer = WordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordDetailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            word = Word.objects.get(
                is_visible=True, dictionary=kwargs['pk'], id=kwargs['word_id'])
        except Word.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = WordSerializer(word, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        try:
            word = Word.objects.get(
                is_visible=True, dictionary=kwargs['pk'], id=kwargs['word_id'])
        except Word.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['author'] = request.user.id
        data['dictionary'] = kwargs["pk"]
        serializer = WordSerializer(word, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            Word.objects.get(
                is_visible=True, dictionary=kwargs['pk'], id=kwargs['word_id']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Word.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def train_word(request, *args, **kwargs):
    word = Word.objects.get(
        is_visible=True, dictionary=kwargs['pk'], id=kwargs['word_id'])

    word.train()
    word.save()

    serializer = WordSerializer(word)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def training(request, *args, **kwargs):

    word_count = Word.objects.filter(
        is_visible=True, dictionary=kwargs['pk']).count() - 1

    random_words = []
    for _ in range(4):
        random_int = random.randint(0, word_count)
        random_word = Word.objects.filter(
            is_visible=True, dictionary=kwargs['pk'], points__lt=100).all()[random_int]
        random_words.append(random_word)

    data = {}

    data["options_words"] = random_words

    serializer = TrainingSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)
