import os

from github import Github

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
g = Github(os.environ.get("GITHUB_TOKEN"))

repo_list = str(os.environ.get("REPO_LIST")).split(", ")
monitoredRepos = []

for repo in repo_list:
    monitoredRepos.append(g.get_repo(repo))


# Stats
def getNumberIssues():
    result = 0

    for repo in monitoredRepos:
        result += len(list(repo.get_issues(state="open")))
    return result


def getNumberPullRequests():
    result = 0

    for repo in monitoredRepos:
        result += len(list(repo.get_pulls(state="open")))
    return result


def getProjects():
    result = []

    # This will need to be changed for the new API
    for repo in monitoredRepos:
        for item in repo.get_issues(state="all"):
            assignees = ""

            state = item.state
            creator = item.user.login

            labels = ""
            for label in item.labels:
                labels += label.name + ", "

            title = item.title
            for assignee in item.assignees:
                assignees = assignees + str(assignee.login) + ", "
            updatedAt = item.updated_at.strftime("%X %x %Z")

            if state != "open":
                result.append(
                    [creator, title, updatedAt, assignees, labels, "TODO", state]
                )
            else:
                result.insert(
                    0, [creator, title, updatedAt, assignees, labels, "TODO", state]
                )

    return result


@app.route("/")
def home_page():
    example_embed = "This string is from python"
    return render_template("index.html", embed=example_embed)


@app.route("/getCurNumbers", methods=["GET", "POST"])
def getCurNumbers():  # GET request

    if request.method == "GET":
        message = {
            "open_pull_requests": getNumberIssues(),
            "open_issues": getNumberPullRequests(),
        }
        return jsonify(message)  # Serialize and return
    if request.method == "POST":
        print(request.get_json())  # parse as JSON
        return "Sucesss", 200


@app.route("/getProjectData", methods=["GET", "POST"])
def getProjectData():  # GET request

    if request.method == "GET":
        return jsonify(getProjects())  # Serialize and return
