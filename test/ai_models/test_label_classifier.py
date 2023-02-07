import pytest

from artificial_intelligence.ai_models.label_classifier import LabelClassifier
from artificial_intelligence.model.issue_type import IssueType


@pytest.fixture
def label_classifier():
    return LabelClassifier(model_path="resources/aiModels/labelModel.joblib")


def test_label_classifier_predict(label_classifier):
    title = "issue title"
    assert label_classifier.predict(title) in IssueType, "Label Classifier does not return an Issue Type"
