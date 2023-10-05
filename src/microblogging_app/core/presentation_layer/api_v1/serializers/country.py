from rest_framework import serializers


class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
