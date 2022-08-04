import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def home_page():
    example_embed = "This string is from python"
    return render_template("index.html", embed=example_embed)


@app.route("/test", methods=["GET", "POST"])
def testfn():  # GET request
    if request.method == "GET":
        message = {"greeting": "Hello from Flask!"}
        return jsonify(message)  # serialize and use JSON headers    # POST request
    if request.method == "POST":
        print(request.get_json())  # parse as JSON
        return "Sucesss", 200
