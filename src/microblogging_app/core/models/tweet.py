"""
"Core" app Tweet model of microblogging_app project.
"""

from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models


class Tweet(BaseModel):
    """Describes the fields and attributes of the Tweet model in the database."""

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="tweets")
    content = models.CharField(max_length=400, null=False)
    reply_to = models.ForeignKey(to="self", on_delete=models.CASCADE, related_name="tweets_replies", null=True)
    like = models.ManyToManyField(to=get_user_model(), through="Like", related_name="tweets_likes")
    repost = models.ManyToManyField(to=get_user_model(), through="Repost", related_name="tweets_reposts")
    tags = models.ManyToManyField(to="Tag", db_table="tweet_tags", related_name="tweets")

    class Meta:
        """Describes class metadata."""

        db_table = "tweets"
