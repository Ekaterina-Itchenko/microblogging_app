import os

from data_access import PostgreSQLGateway
from data_access.dao import (
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
from dotenv import load_dotenv
from factories import (
    FollowersFactory,
    LikeFactory,
    NotificationFactory,
    RepostFactory,
    TagFactory,
    TweetFactory,
    TweetTagsFactory,
    UserFactory,
)
from populate_table_command import PopulateTable
from providers import (
    NotificationMessageProvider,
    PasswordProvider,
    RandomBirthDateProvider,
    RandomDistinctValueFromListProvider,
    RandomTagProvider,
    RandomTextProvider,
    RandomUserProfileProvider,
    RandomValueFromListProvider,
)

load_dotenv()

DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]


def populate_db(num: int) -> None:
    """Populates database with random data."""

    db_gateway = PostgreSQLGateway(db_name=DB_NAME, db_user=DB_USER, db_password=DB_PASSWORD, db_host=DB_HOST)

    tag_dao = TagDAO(db_gateway=db_gateway)
    tag_factory = TagFactory(random_tag_provider=RandomTagProvider())
    PopulateTable(records_number=num, dao=tag_dao, fake_factory=tag_factory).execute()

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

    users_list = UserDAO(db_gateway=db_gateway).get_ids_list()
    tweet_dao = TweetDAO(db_gateway=db_gateway)
    tweet_list = tweet_dao.get_ids_list()
    tweet_factory = TweetFactory(
        random_user_id_provider=RandomValueFromListProvider(values=users_list),
        random_reply_to_provider=RandomValueFromListProvider(values=tweet_list),
        random_text_provider=RandomTextProvider(max_length=400),
    )
    PopulateTable(records_number=num, dao=tweet_dao, fake_factory=tweet_factory).execute()

    tweets_list = TweetDAO(db_gateway=db_gateway).get_ids_list()
    tags_list = TagDAO(db_gateway=db_gateway).get_ids_list()
    tweet_tags_dao = TweetTagsDAO(db_gateway=db_gateway)
    tweet_tags_factory = TweetTagsFactory(
        random_tweets_provider=RandomValueFromListProvider(tweets_list),
        random_tags_provider=RandomValueFromListProvider(tags_list),
    )
    PopulateTable(records_number=num, dao=tweet_tags_dao, fake_factory=tweet_tags_factory).execute()

    reposts_dao = RepostDAO(db_gateway=db_gateway)
    reposts_factory = RepostFactory(
        random_user_provider=RandomValueFromListProvider(values=users_list),
        random_tweet_provider=RandomValueFromListProvider(values=tweets_list),
    )
    PopulateTable(records_number=num, dao=reposts_dao, fake_factory=reposts_factory).execute()

    like_dao = LikeDAO(db_gateway=db_gateway)
    like_factory = LikeFactory(
        random_user_provider=RandomValueFromListProvider(values=users_list),
        random_tweet_provider=RandomValueFromListProvider(values=tweets_list),
    )
    PopulateTable(records_number=num, dao=like_dao, fake_factory=like_factory).execute()

    notification_dao = NotificationDAO(db_gateway=db_gateway)
    notification_types_list = notification_dao.get_notification_type_id_list()
    notification_factory = NotificationFactory(
        notification_message_provider=NotificationMessageProvider(),
        random_user_provider=RandomValueFromListProvider(users_list),
        random_note_type_provider=RandomValueFromListProvider(values=notification_types_list),
    )
    PopulateTable(records_number=num, dao=notification_dao, fake_factory=notification_factory).execute()

    followers_dao = FollowersDAO(db_gateway=db_gateway)
    followers_factory = FollowersFactory(
        random_from_user_provider=RandomValueFromListProvider(users_list),
        random_to_user_provider=RandomDistinctValueFromListProvider(values=users_list),
    )
    PopulateTable(records_number=num, dao=followers_dao, fake_factory=followers_factory).execute()
