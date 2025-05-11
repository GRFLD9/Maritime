def test_create_user_invalid_data(test_client):
    invalid_cases = [
        {"data": {"email": "not-an-email"}, "expected_error": "email"},
        {"data": {"phone": "89161234567"}, "expected_error": "phone"},
        {"data": {"password_hash": "short"}, "expected_error": "password"},
        {"data": {"birth_date": "2023-01-01"}, "expected_error": "birth_date"}
    ]

    for case in invalid_cases:
        response = test_client.post('/api/users', json=case["data"])
        assert response.status_code == 400
        assert "error" in response.json  # Добавляем проверку
        assert case["expected_error"] in str(response.json).lower()


def test_user_authentication(test_client, test_user_data):
    # Создаем пользователя
    test_client.post('/api/users', json=test_user_data)

    # Пытаемся авторизоваться
    auth_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password_hash"]
    }
    response = test_client.post('/api/login', json=auth_data)
    assert response.status_code == 200
    assert "access_token" in response.json