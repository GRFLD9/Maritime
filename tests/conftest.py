import sys
from pathlib import Path

import pytest

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


@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "phone": "+79161234567",
        "password_hash": "secure123",
        "name": "Тест",
        "surname": "Тестов",
        "birth_date": "01.01.1990",
        "city_from": "Москва",
        "is_verified": False,
        "role": "user"
    }


@pytest.fixture(autouse=True)
def clean_db(test_client):
    with test_client.application.app_context():
        from db.database import SqlAlchemyBase
        from db.database import create_session

        db = create_session()
        for table in reversed(SqlAlchemyBase.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()