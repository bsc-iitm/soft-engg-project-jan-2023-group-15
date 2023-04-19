import os
from flask import Flask, redirect
from flask_restful import Api
from application.database import db
# from application import workers
from flask_migrate import Migrate
from flask_cors import CORS
from application import workers
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
    CELERY_ENABLE_UTC = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    REDIS_URL = "redis://localhost:6379"

class LocalDevelopment(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    REDIS_URL = "redis://localhost:6379"

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="")
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

    
    celery = workers.celery
    
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
    )

    celery.Task = workers.ContextTask
    app.app_context().push()

    return app, api, celery

app, api, celery = create_app()

migrate = Migrate(app, db, render_as_batch=True)

from application.api.auth import Login, SupportStaffLogin, SupportStaffRegister, Logout
api.add_resource(Login, '/api/login', methods=['POST'])
api.add_resource(SupportStaffLogin, '/api/support_login', methods=['POST'])
api.add_resource(SupportStaffRegister, '/api/support_register', methods=['POST'])
api.add_resource(Logout, '/api/logout', methods=['POST'])

from application.api.user import UserManagement, BlockedUser, DeactivateUser, UnblockedUser, GetSupportStaff
api.add_resource(UserManagement, '/api/user', methods=['POST', 'GET'])
api.add_resource(BlockedUser, '/api/user/block', methods=['POST'])
api.add_resource(DeactivateUser, '/api/user/deactivate', methods=['POST'])
api.add_resource(UnblockedUser, '/api/user/unblock', methods=['GET', 'POST'])
api.add_resource(GetSupportStaff, '/api/staff', methods=['GET', 'DELETE'])

from application.api.tickets import TicketsAPI, TicketsAll, TicketsFilesDelete, TicketsStaffAll, TicketsUpDownVote, EditStatusTicket, AssignTicket, ReplyToTicket
api.add_resource(TicketsAPI, '/api/ticket', methods=['POST', 'GET', 'PUT', 'DELETE'])
api.add_resource(TicketsAll, '/api/ticket/all', methods=['POST'])
api.add_resource(TicketsStaffAll, '/api/ticket/staff', methods=['GET'])
api.add_resource(TicketsFilesDelete, '/api/ticket/files/delete', methods=['POST'])
api.add_resource(TicketsUpDownVote, '/api/ticket/vote', methods=['POST'])
api.add_resource(EditStatusTicket, '/api/ticket/status', methods=['POST'])
api.add_resource(AssignTicket, '/api/ticket/assign', methods=['POST', 'DELETE'])
api.add_resource(ReplyToTicket, '/api/ticket/reply', methods=['POST', 'PUT', 'DELETE'])

from application.api.tags import TagManagement, SupportStaffTagManagement
api.add_resource(TagManagement, '/api/tag', methods=['POST', 'GET', 'PUT', 'DELETE'])
api.add_resource(SupportStaffTagManagement, '/api/tag/staff', methods=['POST', 'DELETE'])

from application.api.faq import *
api.add_resource(FAQManagement, '/api/faq', methods=['POST', 'GET', 'PUT', 'DELETE'])
api.add_resource(FAQRequest, '/api/faq/request', methods=['POST'])
api.add_resource(FAQAccept, '/api/faq/accept', methods=['POST', 'GET'])
api.add_resource(PinTicket, '/api/ticket/pin', methods=['POST'])


if __name__ == "__main__":
    db.create_all()
    app.run()
