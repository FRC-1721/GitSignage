import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return f"<p>{os.environ.get('GITHUB_TOKEN')}</p>"
