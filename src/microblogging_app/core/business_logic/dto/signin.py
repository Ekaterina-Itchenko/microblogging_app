from dataclasses import dataclass


@dataclass
class SignInDTO:
    email: str
    password: str
