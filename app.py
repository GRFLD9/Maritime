import logging

from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager

from api.resources.booking_resource import BookingResource, BookingListResource
from api.resources.room_resource import RoomListResource, RoomDetailResource
from api.resources.user_resource import (
    UserResource, UsersListResource, RegisterResource, LoginResource
)
from db.database import global_init
from db.repositories.user_repo import UserRepository
from blueprints.user_views import user_blueprint
from blueprints.booking_views import booking_blueprint
from blueprints.room_views import room_blueprint

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
    login_manager.login_view = 'user_views.login'

    @login_manager.user_loader
    def load_user(user_id):
        return UserRepository.get_user_obj_by_id(int(user_id))

    jwt = JWTManager(app)

    api = Api(app)
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(LoginResource, '/login')

    api.add_resource(BookingListResource, '/api/bookings')
    api.add_resource(BookingResource, '/api/bookings/<int:booking_id>')

    api.add_resource(RoomListResource, '/api/rooms')
    api.add_resource(RoomDetailResource, '/api/rooms/<int:room_id>')

    app.register_blueprint(user_blueprint)
    app.register_blueprint(booking_blueprint)
    app.register_blueprint(room_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
