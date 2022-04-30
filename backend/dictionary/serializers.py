from rest_framework import serializers
from .models import Dictionary





class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ("id","language","author","created_at")
        extra_kwargs = {
            'created_at':{'read_only':True}
        }