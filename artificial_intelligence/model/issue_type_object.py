from artificial_intelligence.model.issue_type import IssueType


class IssueTypeObject:
    def __init__(self, issue_type: IssueType):
        self._issue_type = issue_type

    @property
    def issue_type(self):
        return self._issue_type

    @issue_type.setter
    def issue_type(self, other):
        self._issue_type = other

    def to_json(self) -> dict:
        return {
            "issueType": self._issue_type.name
        }
