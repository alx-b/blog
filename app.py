from flask import Flask, Blueprint
import secrets

from routes import routes
from model import db

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.register_blueprint(routes)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


if __name__ == "__main__":
    app.run(debug=True)
