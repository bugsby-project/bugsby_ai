import pytest

from artificial_intelligence.ai_models.offensive_language_classifier import OffensiveLanguageClassifier


@pytest.fixture
def offensive_language_classifier():
    return OffensiveLanguageClassifier(model_path="resources/aiModels/offensiveLanguageModel.joblib")


def test_offensive_language_classifier_predict(offensive_language_classifier):
    text = "flowers are beautiful"
    probability = offensive_language_classifier.predict(text)
    assert float(probability) == probability, "Offensive Language Classifier does not return a float"
