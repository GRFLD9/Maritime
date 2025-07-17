import sys
from pathlib import Path
import pytest
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import create_app
from config import TestingConfig

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestingConfig)
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

@pytest.fixture(autouse=True)
def clean_db(test_client):
    with test_client.application.app_context():
        from db.database import SqlAlchemyBase, create_session
        db = create_session()
        for table in reversed(SqlAlchemyBase.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()

@pytest.fixture
def test_user(test_client):
    user_data = {
        "email": "booking_user@example.com",
        "phone": "+79000000001",
        "password": "testpassword",
        "name": "Тест",
        "surname": "Пользователь",
        "birth_date": "01.01.1990",
        "city_from": "Москва",
        "is_verified": True,
        "role": "user"
    }
    response = test_client.post('/api/users', json=user_data)
    assert response.status_code == 201
    user_json = response.json
    user_json["password"] = user_data["password"]
    return user_json

@pytest.fixture
def test_room(test_client):
    room_data = {
        "name": "Тестовый номер",
        "description": "Комната для тестов",
        "price_per_night": 1000,
        "capacity": 4,
        "amenities": "Wi-Fi, Кондиционер",
        "room_type": "Стандарт"
    }
    response = test_client.post('/api/rooms', json=room_data)
    assert response.status_code == 201
    return response.json

@pytest.fixture
def booking_data(test_room):
    from datetime import datetime, timedelta
    today = datetime.today().date()
    check_in = today + timedelta(days=1)
    check_out = today + timedelta(days=3)
    return {
        "room_id": test_room["id"],
        "check_in": check_in.isoformat(),
        "check_out": check_out.isoformat(),
        "guests": 2
    }


@pytest.fixture
def auth_header(test_client, test_user):
    login_data = {
        "email": test_user["email"],
        "password": "testpassword"
    }
    resp = test_client.post("/login", json=login_data)
    assert resp.status_code == 200, "Login failed during auth_header fixture"
    access_token = resp.json["access_token"]
    return {"Authorization": f"Bearer {access_token}"}

