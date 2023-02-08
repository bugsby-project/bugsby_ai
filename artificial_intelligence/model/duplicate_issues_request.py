from artificial_intelligence.model.issue import Issue
from artificial_intelligence.model.issue_object_list import IssueObjectList


class DuplicateIssuesRequest:
    def __init__(self, project_issues: IssueObjectList, issue: Issue):
        self._project_issues = project_issues
        self._issue = issue

    @property
    def project_issues(self):
        return self._project_issues

    @project_issues.setter
    def project_issues(self, other):
        self._project_issues = other

    @property
    def issue(self):
        return self._issue

    @issue.setter
    def issue(self, other):
        self._issue = other

    def to_json(self) -> dict:
        return {
            "projectIssues": self._project_issues.to_json(),
            "issue": self._issue.to_json()
        }

    @staticmethod
    def from_json(json_dict):
        return DuplicateIssuesRequest(
            project_issues=IssueObjectList.from_json(json_dict["projectIssues"]),
            issue=Issue.from_json(json_dict["issue"])
        )
