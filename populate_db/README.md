# POPULATE_DB script

Populate_db is a Python script for populating a PostgreSQL database of microblogging_app project with random values.

## DEPENDENCIES

For the script to work, you need to install a third-party "faker" library.
You can use package manager [pip](https://pip.pypa.io/en/stable/) to install faker.

```bash
pip install faker
```

If you use special tools for dependency management and packaging in Python (like Poetry), you can yse special
functions for adding new packages like:
```bash
poetry add faker
```
If you want to add dependencies to your project, you can specify them in the [tool.poetry.group.dev.dependencies] section 
```python
[tool.poetry.group.dev.dependencies]
pre-commit = "^3.3.3"
faker = "19.3.0"
```
And the use command:
```bash
poetry install
```

## USAGE

Before using the populate_db script, check if you have a [.env] file in the main project directory with the following data:

```python
DB_NAME = '<postgresql_db_name>'
DB_USER = '<postgresql_db_username>'
DB_PASSWORD = '<postgresql_db_password>'
DB_HOST = '127.0.0.1'
DB_PORT = 5432

LOG_LEVEL = 'INFO'
```

To run the script in the directory where the script is located, run the following command:

```bash
python3 populate_db -n <num_of_generated_data> -t <table_name>
```
AVAILABLE_FLAGS = ('-t', '-n')
After -n flag you can specify number of generated data in the DB.
Flag -n is required!
After -t flag you can specify the table that you want to populate with data.
If you not specify -t flag and table names after it, the script will populate all tables by default.
The following command will add 100 records to each database table:
```bash
python3 populate_db -n 100 
```
The following command will add 100 records to 'users' table:
```bash
python3 populate_db -n 100 -t users
```
The following command will add 100 records to 'users' table and 'tweets' table:
```bash
python3 populate_db -n 100 -t users -t tweets
```
AVAILABLE_TABLES = ("all", "tags", "users", "tweets", "tweet_tags", "likes", "reposts", "notifications", "followers")
If you specify "all" after -t flag, the script will populate all tables.
```bash
python3 populate_db -n 100 -t all
```