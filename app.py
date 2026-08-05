from flask import Flask
import os
from flask_marshmallow import Marshmallow

from db import db, init_db
from util.blueprints import register_blueprint

from models.auth_token import AuthTokens
from models.courses import Courses
from models.lightsabers import Lightsabers
from models.master import Masters
from models.padawan import Padawans
from models.species import Species
from models.temple import Temples
from models.user import Users


flask_host = os.environ.get("FLASK_HOST")
flask_port = os.environ.get("FLASK_PORT")

database_scheme = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"{database_scheme}{database_user}@{database_address}:{database_port}/{database_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)
ma = Marshmallow(app)
register_blueprint(app)


def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully")


if __name__ == "__main__":
    create_tables()
    app.run(host=flask_host, port=flask_port)