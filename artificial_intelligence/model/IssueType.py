from enum import Enum


class IssueType(Enum):
    BUG = 0
    DOCUMENTATION = 1
    ENHANCEMENT = 2
    INVALID = 3
    WONT_FIX = 4
    DUPLICATE = 5
    HELP_WANTED = 6
    QUESTION = 7
