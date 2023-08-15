class UserAlreadyExistsError(Exception):
    ...


class ConfirmationCodeDoesNotExistError(Exception):
    ...


class ConfirmationCodeExpiredError(Exception):
    ...


class InvalidAuthCredentialsError(Exception):
    ...


class UnauthorizedAction(Exception):
    ...


class TweetNotFound(Exception):
    ...
