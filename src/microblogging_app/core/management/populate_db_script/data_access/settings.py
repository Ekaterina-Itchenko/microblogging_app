"""
Contains the settings necessary for the correct operation of the loggers.
"""

import os

from dotenv import load_dotenv

load_dotenv()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console_formatter": {
            "format": "[{asctime}] - {levelname} - {name} - {module}:{funcName}:{lineno} - {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        }
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": os.environ["LOG_LEVEL"],
            "formatter": "console_formatter",
        }
    },
    "loggers": {
        "root": {
            "level": os.environ["LOG_LEVEL"],
            "handlers": ["console_handler"],
        },
    },
}
