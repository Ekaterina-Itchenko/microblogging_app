from __future__ import annotations

from typing import TYPE_CHECKING, Any

from core.management.populate_db_script import populate_db
from django.core.management import BaseCommand

if TYPE_CHECKING:
    from django.core.management.base import CommandParser


class Command(BaseCommand):
    help = (
        "Populates DB by random values.\r\n"
        "Available custom = ('-t', '-n')\n"
        "After -t flag you can specify the table that you want to populate with data.\n"
        "If you not specify -t flag and table names after it, the script will populate all tables by default.\n"
        "The following command will add 100 records to 'users' table and 'tweets' table: "
        ">>>> python3 manage.py -n 100 -t users tweet >>>>. "
    )
    available_tables = (
        "all",
        "tags",
        "users",
        "tweets",
        "tweet_tags",
        "likes",
        "reposts",
        "notifications",
        "followers",
    )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-n",
            "--number",
            type=str,
            help=(
                "Define a number of generated data."
                "After -n flag you can specify number of generated data in the DB."
                "Flag -n is required!"
            ),
        )
        parser.add_argument(
            "-t",
            "--tables",
            nargs="+",
            type=str,
            help=(
                "Define names of table that will be populated. "
                "After -t flag you can specify the table that you want to populate with data."
                "If you not specify -t flag and table names after it, the script will populate all tables by default."
                "Available table names: all, tags, users, tweets, "
                "tweet_tags, likes, reposts, notifications, followers."
            ),
        )

    def handle(self, *args: Any, **options: Any) -> None:
        num: str = options["number"]
        tables: list = options["tables"]
        result_tables = []
        if not num:
            self.stdout.write(self.style.ERROR("Flag -n must be specified."))
        elif not num.isdigit():
            self.stdout.write(self.style.ERROR("After flag -n must be integer value."))
        else:
            number = int(num)
        if not tables or "all" in tables:
            result_tables = ["tags", "users", "tweets", "tweet_tags", "reposts", "likes", "notifications", "followers"]
        else:
            for table in tables:
                if table not in self.available_tables:
                    self.stdout.write(
                        self.style.ERROR(
                            "Unavailable table name. Available tables: "
                            "tags, users, tweets, tweet_tags, reposts, likes, notifications, followers."
                        )
                    )
                else:
                    result_tables.append(table)
        populate_db(num=number, tables=result_tables)
