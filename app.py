import logging
from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from api.resources.user_resource import UserResource, UsersListResource
from db.database import global_init
from db.repositories.user_repo import UserRepository

logging.basicConfig(level=logging.DEBUG)


def create_app(config_object=None):
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    global_init(db_uri)

    app.secret_key = app.config.get("SECRET_KEY", "fallback")

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return UserRepository.get_by_id(int(user_id))

    api = Api(app)
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
