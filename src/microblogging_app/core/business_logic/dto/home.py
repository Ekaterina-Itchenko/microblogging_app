from dataclasses import dataclass
from typing import Optional

from core.models import Tweet


@dataclass
class TweetDTO:
    user: int  # Assuming you pass the user's ID
    content: str
    reply_to: Optional[Tweet] = None  # Pass the tweet instance if it's a reply
    reply_counter: int = 0
