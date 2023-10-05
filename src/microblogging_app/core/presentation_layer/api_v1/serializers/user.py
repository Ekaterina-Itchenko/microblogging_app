from core.presentation_layer.api_v1.validators import APIValidator
from core.presentation_layer.common.validators import ValidateUserAge
from rest_framework import serializers

from .country import CountrySerializer


class UserShortInfoSerialiser(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    photo = serializers.ImageField(max_length=None, allow_empty_file=False)


class UserFullInfoSerialazer(UserShortInfoSerialiser):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    following = UserShortInfoSerialiser()
    birth_date = serializers.DateField()
    country = CountrySerializer()
    description = serializers.CharField(max_length=400, trim_whitespace=True)
    is_active = serializers.BooleanField()
    email = serializers.EmailField()


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50, trim_whitespace=True)
    birth_date = serializers.DateField(validators=[APIValidator(ValidateUserAge(min_age=18))])
    password = serializers.CharField()
