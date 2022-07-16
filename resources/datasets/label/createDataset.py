import sys

import pandas as pd
import requests

urls = {
    "RxJava": {
        "url": "https://api.github.com/repos/ReactiveX/RxJava/issues?state=all&&per_page=100&&page=:page&&"
               "labels=:label",
        "labels": [
            # the label name and the number of pages needed to retrieve all of the issues of that particular label
            ("bug", 8), ("documentation", 6), ("enhancement", 8), ("invalid", 1), ("wont-fix", 1)
        ]
    },
    "netty": {
        "url": "https://api.github.com/repos/netty/netty/issues?state=all&&per_page=100&&page=:page&&labels=:label",
        "labels": [
            ("defect", 27), ("documentation", 2), ("improvement", 12), ("won't fix", 2)
        ]
    },
    "Guava": {
        "url": "https://api.github.com/repos/google/guava/issues?state=all&&per_page=100&&page=:page&&labels=:label",
        "labels": [
            ("type=defect", 5), ("type=documentation", 1), ("type=enhancement", 6), ("status=invalid", 2),
            ("status=will-not-fix", 5)
        ]
    },
    "storio": {
        "url": "https://api.github.com/repos/pushtorefresh/storio/issues?state=all&&per_page=100&&page=:page&&"
               "labels=:label",
        "labels": [
            ("bug", 1), ("enhancement || feature", 7), ("wontfix", 1)
        ]
    },
    "ChartJs": {
        "url": "https://api.github.com/repos/chartjs/chart.js/issues?state=all&&per_page=100&&page=:page&&"
               "labels=:label",
        "labels": [
            ("type: bug", 25), ("type: documentation", 8), ("type: enhancement", 14), ("status: won't fix", 7)
        ]
    },
    "Tensorflow": {
        "url": "https://api.github.com/repos/tensorflow/tensorflow/issues?state=all&&per_page=100&&page=:page&&"
               "labels=:label",
        "labels": [
            ("invalid", 2)
        ]
    },
    "Geany": {
        "url": "https://api.github.com/repos/geany/geany/issues?state=all&&per_page=100&&page=:page&&"
               "labels=:label",
        "labels": [
            ("invalid", 2)
        ]
    },
    "JavaDesignPatterns": {
        "url": "https://api.github.com/repos/iluwatar/java-design-patterns/issues?state=all&&per_page=100&&page=:page&&"
               "labels=:label",
        "labels": [
            ("resolution: invalid", 1), ("resolution: won't fix", 1)
        ]
    }
}

labelMapping = {
    "Bug": "BUG",
    "bug": "BUG",
    "defect": "BUG",
    "type=defect": "BUG",
    "type: bug": "BUG",
    "documentation": "DOCUMENTATION",
    "Documentation": "DOCUMENTATION",
    "type=documentation": "DOCUMENTATION",
    "type: documentation": "DOCUMENTATION",
    "enhancement": "ENHANCEMENT",
    "Enhancement": "ENHANCEMENT",
    "improvement": "ENHANCEMENT",
    "type=enhancement": "ENHANCEMENT",
    "type: enhancement": "ENHANCEMENT",
    "enhancement || feature": "ENHANCEMENT",
    "invalid": "INVALID",
    "Invalid": "INVALID",
    "status=invalid": "INVALID",
    "resolution: invalid": "INVALID",
    "wont-fix": "WONT_FIX",
    "Wont-fix": "WONT_FIX",
    "won't fix": "WONT_FIX",
    "status=will-not-fix": "WONT_FIX",
    "wontfix": "WONT_FIX",
    "status: won't fix": "WONT_FIX",
    "Wont-Fix": "WONT_FIX",
    "resolution: won't fix": "WONT_FIX",
}

token = sys.argv[1]

data = []
for projectName in urls:
    labels = urls[projectName]["labels"]
    for labelNrTuple in labels:
        for i in range(1, labelNrTuple[1] + 1):
            url = urls[projectName]["url"].replace(":page", str(i)).replace(":label", labelNrTuple[0])
            r = requests.get(url, headers={"Authorization": f"token {token}"})
            data.extend(r.json())

# remove the pull requests
data = list(filter(lambda issue: 'pull_request' not in issue, data))

# extract only the necessary data
data = list(map(lambda issue: {"title": issue["title"], "labels": issue["labels"]}, data))

# compute the label
for issueReport in data:
    for label in issueReport["labels"]:
        if label["name"] in labelMapping:
            issueReport["label"] = labelMapping[label["name"]]
            del issueReport["labels"]
            break

df = pd.DataFrame(data, columns=["title", "label"])
df.to_csv("labelDataset.csv", index=True)
