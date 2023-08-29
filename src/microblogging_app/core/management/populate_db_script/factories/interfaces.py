from typing import Protocol


class FakeFactoryProtocol(Protocol):
    """Contains methods for generating values for needed DTO."""

    def generate(self) -> object:
        """Generates random data for needed DTO"""
        raise NotImplementedError
