from artificial_intelligence.model.severity_level import SeverityLevel


class SeverityLevelObject:
    def __init__(self, severity: SeverityLevel):
        self._severity = severity

    @property
    def severity(self):
        return self._severity

    @severity.setter
    def severity(self, other):
        self._severity = other

    def to_json(self) -> dict:
        return {
            "severity": self._severity.name
        }
