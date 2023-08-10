"""
"Core" app Like model of microblogging_app project.
"""

from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models


class Like(BaseModel):
    """Describes the fields and attributes of the Like model in the database."""

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="tweet_likes")
    tweet = models.ForeignKey(to="Tweet", on_delete=models.CASCADE, related_name="likes")

    class Meta:
        """Describes class metadata."""

        db_table = "likes"
        unique_together = [["user", "tweet"]]
