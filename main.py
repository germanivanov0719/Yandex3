from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return "It's working!"


if __name__ == "__main__":
    app.run(port=8000, host="127.0.0.1")
