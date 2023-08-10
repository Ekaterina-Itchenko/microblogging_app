from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datetime import date


@dataclass
class RegistrationDTO:
    email: str
    username: str
    birth_date: date
    password: str

