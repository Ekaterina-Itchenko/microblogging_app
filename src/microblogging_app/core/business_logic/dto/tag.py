from dataclasses import dataclass


@dataclass
class TagDTO:
    """Data transfer object for storing and transferring data from SelectTagForm."""

    tag: str
