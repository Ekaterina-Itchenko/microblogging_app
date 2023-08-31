import os

from core.management.populate_db_script.data_access import PostgreSQLGateway
from core.management.populate_db_script.data_access.dao import (
    CountryDAO,
    FollowersDAO,
    LikeDAO,
    NotificationDAO,
    RepostDAO,
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
    RandomDistinctValueFromListProvider,
    RandomTagProvider,
    RandomTextProvider,
    RandomUserProfileProvider,
    RandomValueFromListOrNoneProvider,
    RandomValueFromListProvider,
)
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

db_gateway = PostgreSQLGateway(
    db_name=DB_NAME, db_user=DB_USER, db_password=DB_PASSWORD, db_host=DB_HOST, db_port=DB_PORT
)


def populate_tag_table(num: int) -> None:
    """Populates tags table with random data."""

    tag_dao = TagDAO(db_gateway=db_gateway)
    tag_factory = TagFactory(random_tag_provider=RandomTagProvider())
    PopulateTable(records_number=num, dao=tag_dao, fake_factory=tag_factory).execute()


def populate_users_table(num: int) -> None:
    """Populates users table with random data."""

    country_dao: CountryDAO = CountryDAO(db_gateway=db_gateway)
    countries_list = country_dao.get_ids_list()
    user_dao = UserDAO(db_gateway=db_gateway)
    user_factory = UserFactory(
        random_country_provider=RandomValueFromListProvider(countries_list),
        random_text_provider=RandomTextProvider(max_length=400),
        random_birth_date_provider=RandomBirthDateProvider(),
        random_profile_provider=RandomUserProfileProvider(),
        password_provider=PasswordProvider(unencrypted_password="password123"),
    )
    PopulateTable(records_number=num, dao=user_dao, fake_factory=user_factory).execute()


def populate_tweet_table(num: int) -> None:
    """Populates tweets table with random data."""

    users_list = UserDAO(db_gateway=db_gateway).get_ids_list()
    if users_list == []:
        raise EmptyDBException("We can't generate new records because users table is empty.")
    tweet_dao = TweetDAO(db_gateway=db_gateway)
    tweet_list = tweet_dao.get_ids_list()
    tweet_factory = TweetFactory(
        random_user_id_provider=RandomValueFromListProvider(values=users_list),
        random_reply_to_provider=RandomValueFromListOrNoneProvider(values=tweet_list),
        random_text_provider=RandomTextProvider(max_length=400),
    )
    PopulateTable(records_number=num, dao=tweet_dao, fake_factory=tweet_factory).execute()


def populate_tweet_tags_table(num: int) -> None:
    """Populates tweet_tags table with random data."""

    tweets_list = TweetDAO(db_gateway=db_gateway).get_ids_list()
    if tweets_list == []:
        raise EmptyDBException("We can't generate new records because tweets table is empty.")
    tags_list = TagDAO(db_gateway=db_gateway).get_ids_list()
    if tags_list == []:
        raise EmptyDBException("We can't generate new records because tags table is empty.")
    tweet_tags_dao = TweetTagsDAO(db_gateway=db_gateway)
    tweet_tags_factory = TweetTagsFactory(
        random_tweets_provider=RandomValueFromListProvider(tweets_list),
        random_tags_provider=RandomValueFromListProvider(tags_list),
    )
    PopulateTable(records_number=num, dao=tweet_tags_dao, fake_factory=tweet_tags_factory).execute()


def populate_reposts_table(num: int) -> None:
    """Populates reposts table with random data."""

    users_list = UserDAO(db_gateway=db_gateway).get_ids_list()
    if users_list == []:
        raise EmptyDBException("We can't generate new records because users table is empty.")
    if len(users_list) == 1:
        raise EmptyDBException(
            "We can't generate new records in reposts table because there is just one record in users table. "
            "User cannot repost their own tweets."
        )
    tweet_dao = TweetDAO(db_gateway=db_gateway)
    tweets_list = tweet_dao.get_ids_list()
    if tweets_list == []:
        raise EmptyDBException("We can't generate new records because tweets table is empty.")
    reposts_dao = RepostDAO(db_gateway=db_gateway)
    reposts_factory = RepostFactory(
        random_user_provider=RandomDistinctValueFromListProvider(values=users_list),
        random_tweet_provider=RandomValueFromListProvider(values=tweets_list),
        tweet_dao=tweet_dao,
    )
    PopulateTable(records_number=num, dao=reposts_dao, fake_factory=reposts_factory).execute()


def populate_likes_table(num: int) -> None:
    """Populates likes table with random data."""

    users_list = UserDAO(db_gateway=db_gateway).get_ids_list()
    if users_list == []:
        raise EmptyDBException("We can't generate new records because users table is empty.")
    if len(users_list) == 1:
        raise EmptyDBException(
            "We can't generate new records in reposts table because there is just one record in users table. "
            "User cannot repost their own tweets."
        )
    tweet_dao = TweetDAO(db_gateway=db_gateway)
    tweets_list = tweet_dao.get_ids_list()
    if tweets_list == []:
        raise EmptyDBException("We can't generate new records because tweets table is empty.")
    like_dao = LikeDAO(db_gateway=db_gateway)
    like_factory = LikeFactory(
        random_user_provider=RandomDistinctValueFromListProvider(values=users_list),
        random_tweet_provider=RandomValueFromListProvider(values=tweets_list),
        tweet_dao=tweet_dao,
    )
    PopulateTable(records_number=num, dao=like_dao, fake_factory=like_factory).execute()


def populate_notifications_table(num: int) -> None:
    """Populates notifications table with notifications from admin."""

    users_list = UserDAO(db_gateway=db_gateway).get_ids_list()
    if users_list == []:
        raise EmptyDBException("We can't generate new records because users table is empty.")
    notification_dao = NotificationDAO(db_gateway=db_gateway)
    notification_type_admin = notification_dao.get_notification_type_id_admin()
    notification_ids_list = notification_dao.get_notification_ids_list()
    if len(notification_ids_list) == 0:
        notification_ids_list.append((1,))
    notification_factory = NotificationFactory(
        notification_message_provider=NotificationMessageProvider(),
        random_user_provider=RandomValueFromListProvider(users_list),
        random_notification_id_provider=RandomValueFromListProvider(notification_ids_list),
        random_note_type_provider=RandomValueFromListProvider([notification_type_admin]),
    )
    PopulateTable(records_number=num, dao=notification_dao, fake_factory=notification_factory).execute()


def populate_followers_table(num: int) -> None:
    """Populates followers table with random data."""

    users_list = UserDAO(db_gateway=db_gateway).get_ids_list()
    if len(users_list) == 0:
        raise EmptyDBException("We can't generate new records in followers table because users table is empty.")
    if len(users_list) == 1:
        raise EmptyDBException(
            "We can't generate new records in followers table because there is just one record in users table."
        )
    followers_dao = FollowersDAO(db_gateway=db_gateway)
    followers_factory = FollowersFactory(
        random_from_user_provider=RandomValueFromListProvider(users_list),
        random_to_user_provider=RandomDistinctValueFromListProvider(values=users_list),
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
