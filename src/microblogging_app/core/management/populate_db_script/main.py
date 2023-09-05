from core.management.populate_db_script.data_access import (
    CountryDAO,
    FollowersDAO,
    LikesDAO,
    NotificationDAO,
    NotificationTypesDAO,
    NotificationUserDAO,
    RepostsDAO,
    TagDAO,
    TweetDAO,
    TweetTagsDAO,
    UserDAO,
)
from core.management.populate_db_script.exceptions import EmptyDBException
from core.management.populate_db_script.factories import (
    FollowersFactory,
    LikeFactory,
    NotificationFactory,
    NotificationUserFactory,
    RepostFactory,
    TagFactory,
    TweetFactory,
    TweetTagsFactory,
    UserFactory,
)
from core.management.populate_db_script.populate_table_command import PopulateTable
from core.management.populate_db_script.providers import (
    NotificationMessageProvider,
    PasswordProvider,
    RandomBirthDateProvider,
    RandomDistinctObjectFromListProvider,
    RandomObjectFromListOrNoneProvider,
    RandomObjectFromListProvider,
    RandomTagProvider,
    RandomTextProvider,
    RandomUserProfileProvider,
)
from core.models import (
    Country,
    Like,
    Notification,
    NotificationType,
    Repost,
    Tag,
    Tweet,
)
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

from microblogging_app.utils import query_debugger

load_dotenv()


@query_debugger
def populate_tag_table(num: int) -> None:
    """Populates tags table with random data."""

    tag_dao = TagDAO(db_model=Tag)
    tag_factory = TagFactory(random_tag_provider=RandomTagProvider())
    PopulateTable(records_number=num, dao=tag_dao, fake_factory=tag_factory).execute()


@query_debugger
def populate_users_table(num: int) -> None:
    """Populates users table with random data."""

    country_dao = CountryDAO(db_model=Country)
    countries_list = country_dao.get_objects_list()
    user_dao = UserDAO(db_model=get_user_model())
    user_factory = UserFactory(
        random_country_provider=RandomObjectFromListProvider(countries_list),
        random_text_provider=RandomTextProvider(max_length=400),
        random_birth_date_provider=RandomBirthDateProvider(),
        random_profile_provider=RandomUserProfileProvider(),
        password_provider=PasswordProvider(unencrypted_password="password123"),
    )
    PopulateTable(records_number=num, dao=user_dao, fake_factory=user_factory).execute()


@query_debugger
def populate_tweet_table(num: int) -> None:
    """Populates tweets table with random data."""

    users_list = UserDAO(db_model=get_user_model()).get_objects_list()
    if users_list == []:
        raise EmptyDBException("We can't generate new records because users table is empty.")
    tweet_dao = TweetDAO(db_model=Tweet)
    tweet_list = tweet_dao.get_objects_list()
    tweet_factory = TweetFactory(
        random_user_id_provider=RandomObjectFromListProvider(values=users_list),
        random_reply_to_provider=RandomObjectFromListOrNoneProvider(values=tweet_list),
        random_text_provider=RandomTextProvider(max_length=400),
    )
    PopulateTable(records_number=num, dao=tweet_dao, fake_factory=tweet_factory).execute()


@query_debugger
def populate_tweet_tags_table(num: int) -> None:
    """Populates tweet_tags table with random data."""

    tweet_dao = TweetDAO(db_model=Tweet)
    tweets_list = tweet_dao.get_objects_list()
    if tweets_list == []:
        raise EmptyDBException("We can't generate new records because tweets table is empty.")
    tags_list = TagDAO(db_model=Tag).get_objects_list()
    if tags_list == []:
        raise EmptyDBException("We can't generate new records because tags table is empty.")
    tweet_tags_dao = TweetTagsDAO(db_model=Tweet.tags.through)
    tweet_tags_factory = TweetTagsFactory(
        random_tweets_provider=RandomObjectFromListProvider(tweets_list),
        random_tags_provider=RandomObjectFromListProvider(tags_list),
    )
    PopulateTable(records_number=num, dao=tweet_tags_dao, fake_factory=tweet_tags_factory).execute()


@query_debugger
def populate_reposts_table(num: int) -> None:
    """Populates reposts table with random data."""

    users_list = UserDAO(db_model=get_user_model()).get_objects_list()
    if users_list == []:
        raise EmptyDBException("We can't generate new records because users table is empty.")
    if len(users_list) == 1:
        raise EmptyDBException(
            "We can't generate new records in reposts table because there is just one record in users table. "
            "User cannot repost their own tweets."
        )
    tweet_dao = TweetDAO(db_model=Tweet)
    tweets_list = tweet_dao.get_objects_list()
    if tweets_list == []:
        raise EmptyDBException("We can't generate new records because tweets table is empty.")
    reposts_dao = RepostsDAO(db_model=Repost)
    reposts_factory = RepostFactory(
        random_user_provider=RandomDistinctObjectFromListProvider(values=users_list),
        random_tweet_provider=RandomObjectFromListProvider(values=tweets_list),
    )
    PopulateTable(records_number=num, dao=reposts_dao, fake_factory=reposts_factory).execute()


@query_debugger
def populate_likes_table(num: int) -> None:
    """Populates likes table with random data."""

    users_list = UserDAO(db_model=get_user_model()).get_objects_list()
    if users_list == []:
        raise EmptyDBException("We can't generate new records because users table is empty.")
    if len(users_list) == 1:
        raise EmptyDBException(
            "We can't generate new records in reposts table because there is just one record in users table. "
            "User cannot repost their own tweets."
        )
    tweet_dao = TweetDAO(db_model=Tweet)
    tweets_list = tweet_dao.get_objects_list()
    if tweets_list == []:
        raise EmptyDBException("We can't generate new records because tweets table is empty.")
    like_dao = LikesDAO(db_model=Like)
    like_factory = LikeFactory(
        random_user_provider=RandomDistinctObjectFromListProvider(values=users_list),
        random_tweet_provider=RandomObjectFromListProvider(values=tweets_list),
    )
    PopulateTable(records_number=num, dao=like_dao, fake_factory=like_factory).execute()


@query_debugger
def populate_notifications_table(num: int) -> None:
    """Populates notifications table with notifications from admin."""

    users_list = UserDAO(db_model=get_user_model()).get_objects_list()
    if users_list == []:
        raise EmptyDBException("We can't generate new records because users table is empty.")
    notification_dao = NotificationDAO(db_model=Notification)
    notification_type_dao = NotificationTypesDAO(db_model=NotificationType)
    admin_notification_type_object = notification_type_dao.get_admin_notification_type_object()
    notification_factory = NotificationFactory(
        notification_message_provider=NotificationMessageProvider(),
        admin_notification_type_object=admin_notification_type_object,
    )
    PopulateTable(records_number=num, dao=notification_dao, fake_factory=notification_factory).execute()
    notifications_list = notification_dao.get_objects_list()
    notification_user_dao = NotificationUserDAO(db_model=Notification.user.through)
    notification_user_factory = NotificationUserFactory(
        random_notification_provider=RandomObjectFromListProvider(notifications_list),
        random_user_provider=RandomObjectFromListProvider(users_list),
    )
    PopulateTable(records_number=num, dao=notification_user_dao, fake_factory=notification_user_factory).execute()


@query_debugger
def populate_followers_table(num: int) -> None:
    """Populates followers table with random data."""

    users_list = UserDAO(db_model=get_user_model()).get_objects_list()
    if len(users_list) == 0:
        raise EmptyDBException("We can't generate new records in followers table because users table is empty.")
    if len(users_list) == 1:
        raise EmptyDBException(
            "We can't generate new records in followers table because there is just one record in users table."
        )
    followers_dao = FollowersDAO(db_model=get_user_model().following.through)
    followers_factory = FollowersFactory(
        random_from_user_provider=RandomObjectFromListProvider(users_list),
        random_to_user_provider=RandomDistinctObjectFromListProvider(values=users_list),
    )
    PopulateTable(records_number=num, dao=followers_dao, fake_factory=followers_factory).execute()


def populate_db(num: int, tables: list[str]) -> None:
    """Populates database with random data."""

    if "tags" in tables:
        populate_tag_table(num=num)
    if "users" in tables:
        populate_users_table(num=num)
    if "tweets" in tables:
        populate_tweet_table(num=num)
    if "tweet_tags" in tables:
        populate_tweet_tags_table(num=num)
    if "reposts" in tables:
        populate_reposts_table(num=num)
    if "likes" in tables:
        populate_likes_table(num=num)
    if "notifications" in tables:
        populate_notifications_table(num=num)
    if "followers" in tables:
        populate_followers_table(num=num)
