import pandas as pd
from joblib import dump
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import ComplementNB

from artificial_intelligence.ai_models.AbstractNLPClassifier import AbstractNLPClassifier
from artificial_intelligence.model.IssueType import IssueType


class LabelClassifier(AbstractNLPClassifier):
    __dataset_path = "resources/datasets/label/labelDataset.csv"

    def __init__(self, model_path: str = None):
        super().__init__(model_path, stopwords.words('english'))

    def train_model(self, path: str):
        """
        Method for training a model for predicting the type of an issue, based on its title
        :param path: the path to save the model to, in addition to its vocabulary and its performance report
        :return:
        """
        self._model_path = path
        issues = pd.read_csv(LabelClassifier.__dataset_path)

        # pre process the data
        issues["title"] = issues["title"].apply(lambda t: self._pre_process_text(t))
        issues["label"] = issues["label"].map(lambda t: IssueType[t].value)

        self._vectorizer = CountVectorizer()
        titles = self._vectorizer.fit_transform(list(issues["title"])).toarray()

        x_train, x_test, y_train, y_test = train_test_split(titles, list(issues["label"]), random_state=0,
                                                            train_size=0.8)

        self._classifier = OneVsRestClassifier(ComplementNB())
        self._classifier.fit(x_train, y_train)
        y_pred = self._classifier.predict(x_test)

        performance = classification_report(y_test, y_pred, labels=issues["label"].unique())

        dump({"model": self._classifier, "vectorizer": self._vectorizer, "performance": performance}, path)

    def predict(self, title: str) -> IssueType:
        """
        Method for predicting the type of a new issue, based on its title
        :param title: the title of the issue
        :return: the predicted IssueType of the issues with the given title
        """
        pre_processed = self._pre_process_text(title)
        bag_of_words = self._vectorizer.transform([pre_processed]).toarray()
        prediction = self._classifier.predict(bag_of_words)[0]
        return IssueType(prediction).name
