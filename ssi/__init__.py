import os

from flask import Flask

from ssi.db import db

app = Flask(__name__)
flask_env = os.getenv("FLASK_ENV")

if flask_env == "development":
    app.config.from_object("ssi.config.DevelopmentConfig")
elif flask_env == "production":
    app.config.from_object("ssi.config.ProductionConfig")

db.init_app(app)

if __name__ == "__main__":
    app.run()
