from enum import Enum


class Severity(Enum):
    TRIVIAL = 0
    MINOR = 1
    MAJOR = 2
    CRITICAL = 3
    BLOCKER = 4
