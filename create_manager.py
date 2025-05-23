from db.database import global_init, create_session
from models.users import User
from werkzeug.security import generate_password_hash

def create_manager():
    global_init("instance/resort.db")
    session = create_session()

    existing = session.query(User).filter(User.email == "manager@example.com").first()
    if existing:
        print("Менеджер уже существует.")
        return

    manager = User(
        email="manager@example.com",
        phone="79990000000",
        name="Марина",
        surname="Менеджерова",
        password_hash=generate_password_hash("securepassword123"),
        role="manager",
        is_verified=True
    )

    session.add(manager)
    session.commit()
    print("Менеджер создан!")

if __name__ == "__main__":
    create_manager()
