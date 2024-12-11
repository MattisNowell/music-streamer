from flask import Flask

app = Flask(__name__)

@app.route("/playlist")
def index():
    return "<p>Hello, world!</p>"

if __name__ == "__main__":
    app.run(debug=True)