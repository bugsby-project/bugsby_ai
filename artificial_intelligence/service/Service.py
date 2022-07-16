from artificial_intelligence.ai_models.LabelClassifier import LabelClassifier
from artificial_intelligence.ai_models.OffensiveLanguageClassifier import OffensiveLanguageClassifier
from artificial_intelligence.ai_models.SeverityClassifier import SeverityClassifier
from artificial_intelligence.ai_models.duplicates_detector import detect
from artificial_intelligence.model.Issue import Issue
from artificial_intelligence.model.IssueType import IssueType
from artificial_intelligence.model.SeverityLevel import SeverityLevel


class Service:
    def __init__(self, severity_classifier: SeverityClassifier,
                 label_classifier: LabelClassifier,
                 offensive_language_classifier: OffensiveLanguageClassifier):
        self.__severity_classifier = severity_classifier
        self.__label_classifier = label_classifier
        self.__offensive_language_classifier = offensive_language_classifier

    def compute_suggested_severity(self, title: str) -> SeverityLevel:
        """
        Method for predicting the severity level of an issue, based on its title, using a pre-trained AI model
        :param title: the title of the issue to be classified
        :return: the predicted severity level of the issue with the corresponding title
        """
        return self.__severity_classifier.predict(title)

    def computed_suggested_type(self, title: str) -> IssueType:
        """
        Method for predicting the issue type of an issue, based on its title, using a pre-trained AI model
        :param title: the title of the issue to be classified
        :return: the predicted issue type of the issue with the corresponding title
        """
        return self.__label_classifier.predict(title)

    def compute_probability_is_offensive(self, text: str) -> float:
        """
        Method for computing the probability of a text to be offensive
        :param text: the text to be classified
        :return: the probability of the given text to be offensive
        """
        return self.__offensive_language_classifier.predict(text)

    def retrieve_duplicate_issues(self, project_issues: list, issue: Issue) -> list:
        """
        Method for retrieving the duplicate issues in a project, given a not-yet-added issue
        :param project_issues: all of the issues of the respective project
        :param issue: the issue that is wished to be compared against project_issues
        :return: a list containing duplicates of issue, members of project_issues
        """
        return detect(corpus=project_issues, document=issue) if project_issues != [] else []
