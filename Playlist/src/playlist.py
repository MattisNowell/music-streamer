from flask import Flask

app = Flask(__name__)

@app.route("/playlist")
def index():
    return "<p>Hello, world!</p>"

@app.route("/playlist/create")
def create():
    return ""

if __name__ == "__main__":
    app.run(debug=True)