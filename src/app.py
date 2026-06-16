import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "hello-world")
APP_VERSION = os.getenv("APP_VERSION", "unknown")


@app.route("/")
def index():
    return jsonify(
        {
            "app": APP_NAME,
            "version": APP_VERSION,
            "status": "ok",
        }
    )


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
