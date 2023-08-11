from dataclasses import dataclass


@dataclass
class RegistrationDTO:
    email: str
    username: str
    birth_date: object
    password: str
