from enum import Enum, auto


class PathKey(Enum):
    """
    Enumeration for different types of paths used in the file system.

    Attributes
    ----------
    RESULTS : auto
        Represents the path for storing results.
    DATA : auto
        Represents the path for storing data.
    METRICS : auto
        Represents the path for storing metrics.
    """
    RESULTS = auto()
    DATA = auto()
    METRICS = auto()
