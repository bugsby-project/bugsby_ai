import pytest

from artificial_intelligence.ai_models.SeverityClassifier import SeverityClassifier
from artificial_intelligence.model.SeverityLevel import SeverityLevel


@pytest.fixture
def severity_classifier():
    return SeverityClassifier(model_path="resources/aiModels/severityModel.joblib")


def test_severity_classifier_predict(severity_classifier):
    title = "the database is lost"
    assert severity_classifier.predict(title) in SeverityLevel, "Severity Classifier not predicting severity levels"
