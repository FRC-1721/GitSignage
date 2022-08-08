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
    for repo in monitoredRepos:
        for project in repo.get_projects():
            for column in project.get_columns():
                for card in column.get_cards():
                    print("============")
                    print(card.creator)
                    if (card.note == None):
                        print(card.get_content().title)
                        print(card.get_content().assignees)
                    else:
                        print(card.note)
                    print(card.updated_at)
                    print(card.archived)
                    print("============")



@app.route("/")
def home_page():
    example_embed = "This string is from python"
    return render_template("index.html", embed=example_embed)


@app.route("/getCurNumbers", methods=["GET", "POST"])
def testfn():  # GET request

    if request.method == "GET":
        message = {
            "open_pull_requests": getNumberIssues(),
            "open_issues": getNumberPullRequests(),
        }
        return jsonify(message)  # Serialize and return
    if request.method == "POST":
        print(request.get_json())  # parse as JSON
        return "Sucesss", 200
