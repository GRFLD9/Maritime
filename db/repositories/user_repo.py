from sqlalchemy.exc import IntegrityError
from models.users import User
from db.database import create_session
from exceptions import ValidationError


class UserRepository:
    @staticmethod
    def _serialize_user(user: User) -> dict:
        return user.to_dict(rules=User.get_serialize_rules())

    @staticmethod
    def get_by_id(user_id: int) -> dict | None:
        with create_session() as session:
            user = session.get(User, user_id)
            return UserRepository._serialize_user(user) if user else None

    @staticmethod
    def create_user(data: dict) -> dict:
        with create_session() as session:
            try:
                user = User(**data)
                session.add(user)
                session.commit()
                session.refresh(user)
                return UserRepository._serialize_user(user)
            except IntegrityError as e:
                session.rollback()
                if 'email' in str(e):
                    raise ValidationError("Email уже занят")
                elif 'phone' in str(e):
                    raise ValidationError("Телефон уже занят")
                raise

    @staticmethod
    def update_user(user_id: int, data: dict) -> dict | None:
        with create_session() as session:
            user = session.get(User, user_id)
            if not user:
                return None

            for key, value in data.items():
                setattr(user, key, value)

            session.commit()
            return UserRepository._serialize_user(user)

    @staticmethod
    def delete_user(user_id: int) -> bool:
        with create_session() as session:
            user = session.get(User, user_id)
            if not user:
                return False
            session.delete(user)
            session.commit()
            return True

    @staticmethod
    def get_all() -> list[dict]:
        with create_session() as session:
            users = session.query(User).all()
            return [UserRepository._serialize_user(u) for u in users]