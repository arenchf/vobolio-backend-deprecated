from rest_framework import serializers

from word.models import Word
from word.serializers import WordSerializer
from .models import Dictionary


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ("id", "language", "name", "author", "created_at")
        extra_kwargs = {
            'id': {"read_only": True},
            # 'author': {"read_only": True},
            'created_at': {'read_only': True}
        }


class DetailedDictionarySerializer(serializers.ModelSerializer):

    words = serializers.SerializerMethodField()

    class Meta:
        model = Dictionary
        fields = ("id", "language", "name", "author", "words", "created_at")
        extra_kwargs = {
            'id': {"read_only": True},
            'author': {"read_only": True},
            'created_at': {'read_only': True}
        }

    def get_words(self, obj):
        query = Word.objects.filter(is_visible=True, dictionary=obj.id)
        words_count = query.count()
        learned_words = query.filter(points__gte=100).count()

        return {
            "total": words_count,
            "learned": learned_words
        }
