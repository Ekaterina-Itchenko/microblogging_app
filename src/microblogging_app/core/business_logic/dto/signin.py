from dataclasses import dataclass


@dataclass
class SignInDTO:
    """Data transfer object for storing and transferring data from SignInForm."""

    email: str
    password: str
