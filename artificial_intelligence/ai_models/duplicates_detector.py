from nltk import WordNetLemmatizer, pos_tag
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from artificial_intelligence.model.Issue import Issue

__limit = 5
__threshold = 0.2


def _get_wordnet_pos(treebank_tag):
    """
    Method for converting a TreeBank tag to a WordNet POS tag
    :param treebank_tag: the tag to convert
    :return: the converted tag (WordNet format)
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def _lemmatize_sentence(sentence: str) -> str:
    """
    Method for lemmatizing a sentence
    :param sentence: the sentence to lemmatize
    :return: the lemmatized form of the sentence
    """
    wnl = WordNetLemmatizer()
    words = sentence.split(' ')
    return " ".join([wnl.lemmatize(word=word, pos=_get_wordnet_pos(pos_tag([word])[0][1])) for word in words])


def detect(corpus: list, document: Issue) -> list:
    """
    Method for retrieving the most similar issues to another issue
    :param corpus: a collection representing the available issues
    :param document: the issue to compare to
    :return: a list of the most similar issues from corpus to document
    """
    # hold the original titles (before pre-processing) in a separate variable
    original_titles = dict(map(lambda _issue: (_issue.id, _issue.title), corpus))
    original_document_title = document.title

    # pre-processing
    document.title = _lemmatize_sentence(document.title)
    for issue in corpus:
        issue.title = _lemmatize_sentence(issue.title)

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(corpus)
    y = vectorizer.transform([document])

    similarities = [(cosine_similarity([X.toarray()[i]], y.toarray())[0][0], doc)
                    for i, doc in enumerate(corpus)]
    similarities = list(filter(lambda x: x[0] > __threshold, similarities))
    similarities.sort(key=lambda x: x[0], reverse=True)

    similar_issues = list(map(lambda x: x[1], similarities))
    # change the titles of the issues to the original ones
    document.title = original_document_title
    for issue in similar_issues:
        issue.title = original_titles[issue.id]

    return similar_issues[:__limit]
