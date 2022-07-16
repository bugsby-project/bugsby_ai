from artificial_intelligence.model.IssueType import IssueType
from artificial_intelligence.model.Severity import Severity
from artificial_intelligence.model.Status import Status


class Issue:
    def __init__(self, identifier: int, title: str, description: str,
                 severity: Severity, status: Status, issue_type: IssueType):
        self._id = identifier
        self._title = title
        self._description = description
        self._severity = severity
        self._status = status
        self._type = issue_type

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, other):
        self._title = other

    @property
    def description(self):
        return self._description

    @property
    def severity(self):
        return self._severity

    @property
    def status(self):
        return self._status

    @property
    def type(self):
        return self._type

    def lower(self):
        return self._title.lower()

    def __str__(self):
        return self._title

    def to_json(self) -> dict:
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "status": self._status.name,
            "severity": self._severity.name,
            "type": self._type.name
        }

    @staticmethod
    def from_json(json_dict):
        return Issue(identifier=json_dict["id"],
                     title=json_dict["title"],
                     description=json_dict["description"],
                     status=Status[json_dict["status"]],
                     severity=Severity[json_dict["severity"]],
                     issue_type=IssueType[json_dict["type"]])
