"""
"Core" app Tweet model of microblogging_app project.
"""

from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models


class Tweet(BaseModel):
    """Describes the fields and attributes of the Tweet model in the database."""

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="tweet")
    content = models.CharField(max_length=400, null=False)
    reply_to = models.ForeignKey(to="self", on_delete=models.CASCADE, related_name="tweet_reply")
    reply_counter = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(to=get_user_model(), through="Like", related_name="tweet_likes")
    reposts = models.ManyToManyField(to=get_user_model(), through="Repost", related_name="tweet_reposts")
    tags = models.ManyToManyField(to="Tag", db_table="tweet_tags", related_name="tweet")

    def number_of_likes(self) -> int:
        """Counts the number of likes of a specific tweet."""

        result: int = self.likes.count()
        return result

    def number_of_reposts(self) -> int:
        """Counts the number of reposts of a specific tweet."""

        result: int = self.reposts.count()
        return result

    class Meta:
        """Describes class metadata."""

        db_table = "tweets"
