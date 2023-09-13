from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create flask app
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "idjwejnvegd"  # optional

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app