import os
import sys

from main import populate_db

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
AVAILABLE_FLAGS = ("-n", "-t")
AVAILABLE_TABLES = ("all", "tags", "users", "tweets", "tweet_tags", "likes", "reposts", "notifications", "followers")

if __name__ == "__main__":
    config_list = sys.argv
    flags = config_list[1::2]
    if "-n" not in flags:
        raise ValueError("The '-n' flag must always be specified!")
    if len(flags) == 1:
        tables = ["tags", "users", "tweets", "tweet_tags", "reposts", "likes", "notifications", "followers"]
    else:
        tables = []
    for ind in range(1, len(config_list), 2):
        flag = config_list[ind]
        if flag not in AVAILABLE_FLAGS:
            raise ValueError('Invalid flag. Available flags: "-n", "-t".')
        elif flag == "-n":
            num_data = config_list[ind + 1]
        elif flag == "-t":
            table = config_list[ind + 1]
            if table not in AVAILABLE_TABLES:
                raise ValueError(
                    'Invalid table name. Available values: "all", "tags", "users", "tweets",'
                    ' "tweet_tags", "likes", "reposts", "notifications", "followers"'
                )
            elif table == "all":
                tables = ["tags", "users", "tweets", "tweet_tags", "reposts", "likes", "notifications", "followers"]
            elif table not in tables:
                tables.append(table)
    if not num_data.isalnum():
        raise ValueError('Number of generated data after flag "-n" must be ' "integer.")
    generate_number = int(num_data)
    populate_db(num=generate_number, tables=tables)
