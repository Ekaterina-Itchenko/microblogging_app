from dataclasses import dataclass


@dataclass
class RegistrationDTO:
    """Data transfer object for storing and transferring data from RegistrationForm."""

    email: str
    username: str
    birth_date: object
    password: str
