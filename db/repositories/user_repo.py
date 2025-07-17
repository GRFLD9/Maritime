from sqlalchemy.exc import IntegrityError

from db.database import create_session
from exceptions import ValidationError
from models.users import User


class UserRepository:
    @staticmethod
    def serialize_user(user: User) -> dict:
        return user.to_dict(rules=User.get_serialize_rules())

    @staticmethod
    def get_by_id(user_id: int) -> dict | None:
        with create_session() as session:
            user = session.get(User, user_id)
            return UserRepository.serialize_user(user) if user else None

    @staticmethod
    def get_user_obj_by_id(user_id: int) -> User | None:
        with create_session() as session:
            return session.get(User, user_id)

    @staticmethod
    def create_user(data: dict) -> dict:
        with create_session() as session:
            try:
                user = User(**data)
                session.add(user)
                session.commit()
                session.refresh(user)
                return UserRepository.serialize_user(user)
            except IntegrityError as e:
                print("IntegrityError:", e.orig)
                session.rollback()
                msg = str(e.orig).lower()
                if 'email' in msg:
                    raise ValidationError("Email уже занят")
                elif 'phone' in msg:
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
            return UserRepository.serialize_user(user)

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
            return [UserRepository.serialize_user(u) for u in users]

    @staticmethod
    def get_serialized_user_with_password_by_email_or_phone(identifier: str) -> tuple[User, dict] | None:
        with create_session() as session:
            user = session.query(User).filter(
                (User.email == identifier) | (User.phone == identifier)
            ).first()
            if not user:
                return None
            serialized = user.to_dict(rules=User.get_serialize_rules())
            return user, serialized
