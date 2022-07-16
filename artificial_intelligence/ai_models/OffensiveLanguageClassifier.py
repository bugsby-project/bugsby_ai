import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from artificial_intelligence.ai_models.AbstractNLPClassifier import AbstractNLPClassifier


class OffensiveLanguageClassifier(AbstractNLPClassifier):
    __dataset_path = "resources/datasets/offensiveLanguage/clean_data.csv"

    def __init__(self, model_path: str = None):
        super().__init__(model_path, [])

    def train_model(self, path: str):
        """
        Method for training a model for identifying offensive language within a text
        :param path: the path to save the model and its vocabulary
        :return:
        """
        self._model_path = path
        data = pd.read_csv(OffensiveLanguageClassifier.__dataset_path)

        texts = data['text'].astype(str)
        y = data['is_offensive']

        self._vectorizer = CountVectorizer(stop_words='english', min_df=0.0001)
        X = self._vectorizer.fit_transform(texts)

        model = MultinomialNB()
        self._classifier = CalibratedClassifierCV(base_estimator=model)
        self._classifier.fit(X, y)

        joblib.dump({"model": self._classifier, "vectorizer": self._vectorizer}, path)

    def predict(self, text: str) -> float:
        """
        Method for identifying identifying offensive language within a text
        :param text: the text to identify offensive language from
        :return: the probability of the given text to be offensive
        """
        vectorized = self._vectorizer.transform([text])
        return np.apply_along_axis(lambda x: x[1], 1, self._classifier.predict_proba(vectorized))[0]
