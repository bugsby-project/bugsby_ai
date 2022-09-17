import nltk
import pytest


@pytest.fixture(scope="session", autouse=True)
def set_up():
    try:
        nltk.data.find('stopwords')
        nltk.data.find('wordnet')
        nltk.data.find('omw-1.4')
        nltk.data.find('averaged_perceptron_tagger')
    except LookupError:
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        nltk.download('averaged_perceptron_tagger')
