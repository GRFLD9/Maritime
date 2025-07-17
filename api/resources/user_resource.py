from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from utils.decorators import jwt_role_required

from api.parsers.user_parser import create_parser, update_parser, login_parser
from exceptions import UserNotFoundError, ValidationError
from services.user_service import UserService


class UserResource(Resource):
    @jwt_required()
    @jwt_role_required('admin')
    def get(self, user_id):
        """Получить пользователя по ID"""
        try:
            user = UserService.get_user(user_id)
            return user, 200
        except UserNotFoundError as e:
            return {"error": str(e)}, 404

    @jwt_required()
    @jwt_role_required('admin')
    def put(self, user_id):
        """Обновить пользователя"""
        try:
            args = update_parser.parse_args()
            update_data = {k: v for k, v in args.items() if v is not None}
            user = UserService.update_user(user_id, update_data)
            return user, 200
        except (UserNotFoundError, ValidationError) as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @jwt_role_required('admin')
    def delete(self, user_id):
        """Удалить пользователя"""
        try:
            UserService.delete_user(user_id)
            return "", 204
        except UserNotFoundError as e:
            return {"error": str(e)}, 404


class UsersListResource(Resource):
    @jwt_required()
    @jwt_role_required('admin')
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
            user = UserService.create_user(args)
            return user, 201
        except ValidationError as e:
            return {"error": str(e)}, 400


class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        identifier = args.get("email") or args.get("phone")
        password = args.get("password")

        if not identifier or not password:
            return {"error": "Email или телефон и пароль обязательны"}, 400

        try:
            user = UserService.authenticate_user(identifier, password)
            access_token = create_access_token(identity=str(user["id"]))
            return {"access_token": access_token}, 200
        except ValidationError as e:
            return {"error": str(e)}, 401
