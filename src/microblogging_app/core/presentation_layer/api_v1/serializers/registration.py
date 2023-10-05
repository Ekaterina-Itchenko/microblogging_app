from rest_framework import serializers


class RegistrationSerialiser(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    birth_date = serializers.DateField()
    password = serializers.CharField()
