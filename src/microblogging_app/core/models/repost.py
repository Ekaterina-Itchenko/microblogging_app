"""
"Core" app Repost model of microblogging_app project.
"""

from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models


class Repost(BaseModel):
    """Describes the fields and attributes of the Repost model in the database."""

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="tweet_reposts")
    tweet = models.ForeignKey(to="Tweet", on_delete=models.CASCADE, related_name="reposts")

    class Meta:
        """Describes class metadata."""

        db_table = "reposts"
        unique_together = [["user", "tweet"]]
