from datetime import timedelta
import os
from flask import Flask, redirect
from flask_restful import Api
from application.database import db
# from application import workers
from flask_migrate import Migrate
from flask_cors import CORS
# from application.models.user_mode import Role, User
# from flask_sse import sse

app = celery= None
api = None

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLITE_DB = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


class LocalDevelopment(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="", static_url_path="")
    app.logger.debug("Starting Server")
    app.config.from_object(LocalDevelopment)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SECRET_KEY'] = '21f1004451abcd.'
    app.config['SECURITY_PASSWORD_SALT'] = "21f100##4451@$"
    db.init_app(app)
    

    app.app_context().push()
    # user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    # security = Security(app, user_datastore)
    api = Api(app)
    CORS(app)

    return app, api, celery

app, api, celery = create_app()

migrate = Migrate(app, db, render_as_batch=True)

from application.api.auth import Login
api.add_resource(Login, '/api/login', methods=['POST'])

from application.api.user import UserManagement
api.add_resource(UserManagement, '/api/user', methods=['POST', 'GET'])

if __name__ == "__main__":
    db.create_all()
    app.run()
