from artificial_intelligence.model.issue import Issue


class IssueObjectList:
    def __init__(self, issues: list):
        self._issues = issues

    @property
    def issues(self):
        return self._issues

    @issues.setter
    def issues(self, other):
        self._issues = other

    def to_json(self) -> dict:
        return {
            "issues": list(map(lambda issue: issue.to_json(), self._issues))
        }

    @staticmethod
    def from_json(json_dict):
        return IssueObjectList(
            issues=list(map(lambda issue: Issue.from_json(issue), list(json_dict["issues"])))
        )
