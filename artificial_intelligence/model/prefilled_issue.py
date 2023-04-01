from artificial_intelligence.model.issue_type import IssueType
from artificial_intelligence.model.severity import Severity


class PrefilledIssue:
    def __init__(self, title: str, description: str, expected_behaviour: str, actual_behaviour: str,
                 stack_trace: str, severity: Severity, issue_type: IssueType):
        self._title = title
        self._description = description
        self._expected_behaviour = expected_behaviour
        self._actual_behaviour = actual_behaviour
        self._stack_trace = stack_trace
        self._severity = severity
        self._type = issue_type

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def expected_behaviour(self):
        return self._description

    @property
    def actual_behaviour(self):
        return self._description

    @property
    def stack_trace(self):
        return self._description

    @property
    def severity(self):
        return self._severity

    @property
    def type(self):
        return self._type

    def to_json(self) -> dict:
        return {
            "title": self._title,
            "description": self._description,
            "expectedBehaviour": self._expected_behaviour,
            "actualBehaviour": self._actual_behaviour,
            "stackTrace": self._stack_trace,
            "severity": self._severity.name,
            "type": self._type.name
        }