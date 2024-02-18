import os

import nltk
from nltk.corpus import wordnet
from flask import Flask, request, jsonify

from artificial_intelligence.ai_models.label_classifier import LabelClassifier
from artificial_intelligence.ai_models.offensive_language_classifier import OffensiveLanguageClassifier
from artificial_intelligence.ai_models.severity_classifier import SeverityClassifier
from artificial_intelligence.log_parser.gradle_log_parser import GradleLogParser
from artificial_intelligence.model.duplicate_issues_request import DuplicateIssuesRequest
from artificial_intelligence.model.issue_object_list import IssueObjectList
from artificial_intelligence.model.issue_type_object import IssueTypeObject
from artificial_intelligence.model.probability_object import ProbabilityObject
from artificial_intelligence.model.severity_level_object import SeverityLevelObject
from artificial_intelligence.service.service import Service


def __install_packages():
    """
    Method for installing the necessary packaged from the nltk library
    :return:
    """
    wordnet.ensure_loaded()
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
gradle_log_parser = GradleLogParser(severity_classifier)


@app.route("/suggested-severity")
def get_suggested_severity():
    title = request.args.get("title")
    result = service.compute_suggested_severity(title)
    return jsonify(SeverityLevelObject(result).to_json())


@app.route("/suggested-type")
def get_suggested_type():
    title = request.args.get("title")
    result = service.computed_suggested_type(title)
    return jsonify(IssueTypeObject(result).to_json())


@app.route("/is-offensive")
def get_probability_is_offensive():
    text = request.args.get("text")
    result = service.compute_probability_is_offensive(text)
    return jsonify(ProbabilityObject(result).to_json())


@app.route("/duplicate-issues", methods=['POST'])
def retrieve_duplicate_issues():
    data = request.json
    duplicate_issues_request = DuplicateIssuesRequest.from_json(data)
    result = service.retrieve_duplicate_issues(duplicate_issues_request.project_issues.issues,
                                               duplicate_issues_request.issue)
    issue_object_list_result = IssueObjectList(result)
    return jsonify(issue_object_list_result.to_json())


@app.route("/log-analysis", methods=['POST'])
def analyse_log_file():
    title = request.form.get('title')
    file_request = request.files['logFile']
    prefilled_issue = gradle_log_parser.analyse_log(title, file_request)
    return jsonify(prefilled_issue.to_json())


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=True, host="0.0.0.0", port=port)
