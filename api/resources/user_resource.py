from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from api.parsers.user_parser import create_parser, update_parser
from exceptions import UserNotFoundError, ValidationError
from services.user_service import UserService


class UserResource(Resource):
    def get(self, user_id):
        """Получить пользователя по ID"""
        try:
            user = UserService.get_user(user_id)
            return user, 200
        except UserNotFoundError as e:
            return {"error": str(e)}, 404

    def put(self, user_id):
        """Обновить пользователя"""
        try:
            args = update_parser.parse_args()
            update_data = {k: v for k, v in args.items() if v is not None}
            user = UserService.update_user(user_id, update_data)
            return user, 200
        except (UserNotFoundError, ValidationError) as e:
            return {"error": str(e)}, 400

    def delete(self, user_id):
        """Удалить пользователя"""
        try:
            UserService.delete_user(user_id)
            return "", 204
        except UserNotFoundError as e:
            return {"error": str(e)}, 404


class UsersListResource(Resource):
    def get(self):
        """Получить всех пользователей"""
        users = UserService.get_all_users()
        return {"users": users}, 200

    def post(self):
        """Создать нового пользователя"""
        try:
            args = create_parser.parse_args()
            user = UserService.create_user(args)
            return user, 201
        except ValidationError as e:
            return {"error": str(e)}, 400


class RegisterResource(Resource):
    def post(self):
        try:
            args = create_parser.parse_args()
            user = UserService.register_user(args)
            return user, 201
        except ValidationError as e:
            return {"error": str(e)}, 400


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        identifier = data.get("email") or data.get("phone")
        password = data.get("password")

        if not identifier or not password:
            return {"error": "Email или телефон и пароль обязательны"}, 400

        try:
            user = UserService.authenticate_user(identifier, password)
            access_token = create_access_token(identity=user["id"])
            return {"access_token": access_token}, 200
        except ValidationError as e:
            return {"error": str(e)}, 401
