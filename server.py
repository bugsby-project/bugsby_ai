import os

import nltk
from flask import Flask, request, jsonify

from artificial_intelligence.ai_models.LabelClassifier import LabelClassifier
from artificial_intelligence.ai_models.OffensiveLanguageClassifier import OffensiveLanguageClassifier
from artificial_intelligence.ai_models.SeverityClassifier import SeverityClassifier
from artificial_intelligence.model.Issue import Issue
from artificial_intelligence.service.Service import Service


def __install_packages():
    """
    Method for installing the necessary packaged from the nltk library
    :return:
    """
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


app = Flask("Bugsby Artificial Intelligence API")
__install_packages()
severity_classifier = SeverityClassifier("resources/aiModels/severityModel.joblib")
label_classifier = LabelClassifier("resources/aiModels/labelModel.joblib")
offensive_language_classifier = OffensiveLanguageClassifier("resources/aiModels/offensiveLanguageModel.joblib")
service = Service(severity_classifier, label_classifier, offensive_language_classifier)


@app.route("/suggested-severity")
def get_suggested_severity():
    title = request.args.get("title")
    result = service.compute_suggested_severity(title)
    return result.name


@app.route("/suggested-type")
def get_suggested_type():
    title = request.args.get("title")
    return service.computed_suggested_type(title)


@app.route("/is-offensive")
def get_probability_is_offensive():
    text = request.args.get("text")
    return str(service.compute_probability_is_offensive(text))


@app.route("/duplicate-issues", methods=['POST'])
def retrieve_duplicate_issues():
    data = request.json
    project_issues = [Issue.from_json(issue_json) for issue_json in data["projectIssues"]]
    issue = Issue.from_json(data["issue"])
    result = service.retrieve_duplicate_issues(project_issues, issue)
    return jsonify([issue.to_json() for issue in result])


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=True, host="0.0.0.0", port=port)
