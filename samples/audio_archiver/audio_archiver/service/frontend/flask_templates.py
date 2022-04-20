from flask import Flask
from flask.templating import render_template
from utils.config import CONFIG, TEMPLATES_DIR

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")


def run_templates():
    app.run(
        debug=True,
        host=CONFIG.get("flask").get("host"),
        port=CONFIG.get("flask").get("port"),
    )

