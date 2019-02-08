from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/api/hello")
def hello():
    return jsonify({"text": "Hello"})
