import pandas as pd
from joblib import dump
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB

from artificial_intelligence.ai_models.AbstractNLPClassifier import AbstractNLPClassifier
from artificial_intelligence.model.SeverityLevel import SeverityLevel


class SeverityClassifier(AbstractNLPClassifier):
    __approved_stopwords = ["no", "not", "nor"]
    __dataset_path = "resources/datasets/severity/severityDataset.csv"

    def __init__(self, model_path: str = None):
        stop_words = [word for word in stopwords.words('english')
                      if word not in SeverityClassifier.__approved_stopwords]
        super().__init__(model_path, stop_words)

    def train_model(self, path: str):
        """
        Method for training a model for predicting the severity level of an issue, based on its title
        :param path: the path to save the model to, in addition to its vocabulary and its performance report
        :return:
        """
        self._model_path = path
        issues = pd.read_csv(SeverityClassifier.__dataset_path)

        # pre process the data
        issues["Summary"] = issues["Summary"].apply(lambda t: self._pre_process_text(t))
        issues["Priority"] = issues["Priority"].map({"Trivial": SeverityLevel.non_severe.name,
                                                     "Minor": SeverityLevel.non_severe.name,
                                                     "Major": SeverityLevel.non_severe.name,
                                                     "Critical": SeverityLevel.severe.name,
                                                     "Blocker": SeverityLevel.severe.name})

        self._vectorizer = CountVectorizer()
        summary = self._vectorizer.fit_transform(list(issues["Summary"])).toarray()

        x_train, x_test, y_train, y_test = train_test_split(summary, list(issues["Priority"]), random_state=0,
                                                            train_size=0.8)

        self._classifier = ComplementNB()
        self._classifier.fit(x_train, y_train)
        y_pred = self._classifier.predict(x_test)

        performance = classification_report(y_test, y_pred, target_names=issues["Priority"].unique())

        dump({"model": self._classifier, "vectorizer": self._vectorizer, "performance": performance}, path)

    def predict(self, title: str) -> SeverityLevel:
        """
        Method for predicting the severity level of a new issue, based on its title
        :param title: the title of the issue
        :return: the predicted SeverityLevel of the issues with the given title
        """
        pre_processed = self._pre_process_text(title)
        bag_of_words = self._vectorizer.transform([pre_processed]).toarray()
        prediction = self._classifier.predict(bag_of_words)[0]
        return SeverityLevel[prediction]
