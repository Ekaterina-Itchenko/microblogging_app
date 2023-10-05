from rest_framework import serializers


class TagSerialiser(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
