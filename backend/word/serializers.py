from rest_framework import serializers
from .models import Word,Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","author","dictionary"]
        extra_kwargs = {'id': {'read_only': True}}


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["id","word","translation","created_at","updated_at","points","author","dictionary","category"]
        extra_kwargs = {
                            'id': {'read_only': True},
                            'points':{'read_only':True}
                        }