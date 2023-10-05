from core.presentation_layer.api_v1.validators import APIValidator
from core.presentation_layer.common.validators import ValidateMaxTagCount
from rest_framework import serializers

from .tag import TagSerialiser
from .user import UserShortInfoSerialiser


class TweetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()
    user = UserShortInfoSerialiser()
    num_reposts = serializers.IntegerField()
    num_likes = serializers.IntegerField()
    num_replies = serializers.IntegerField()
    tags = TagSerialiser(many=True)
    repost = UserShortInfoSerialiser(many=True)
    created_at = serializers.DateTimeField()
    like = UserShortInfoSerialiser(many=True)


class CreateTweetSerialiser(serializers.Serializer):
    content = serializers.CharField(max_length=400, trim_whitespace=True)
    tags = serializers.CharField(
        max_length=100, validators=[APIValidator(ValidateMaxTagCount(max_count=20))], required=False
    )


class EditTweetSerialiser(serializers.Serializer):
    content = serializers.CharField(max_length=400, trim_whitespace=True)
    tags = serializers.CharField(
        max_length=100, validators=[APIValidator(ValidateMaxTagCount(max_count=20))], required=False
    )


class TweetResponseSerialiser(serializers.Serializer):
    message = serializers.CharField(max_length=400, trim_whitespace=True)
    tweet_id = serializers.IntegerField()
