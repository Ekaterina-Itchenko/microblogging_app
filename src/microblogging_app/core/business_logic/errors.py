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


class TweetAlreadyLikedByUserError(Exception):
    ...


class TweetAlreadyRepostedByUserError(Exception):
    ...


class TagNotFound(Exception):
    ...


class CountryNotEnteredError(Exception):
    ...
