def test_login_by_email_and_phone(test_client):
    user_data = {
        "email": "login_test@example.com",
        "phone": "+79001112233",
        "password": "supersecurepassword",
        "name": "Логин",
        "surname": "Тестов",
        "birth_date": "01.01.1990",
        "city_from": "Москва",
        "is_verified": True,
        "role": "user"
    }

    # Регистрация пользователя
    response = test_client.post('/api/users', json=user_data)
    print(response.json)  # добавь в тесте сразу после ответа
    assert response.status_code == 201

    assert "id" in response.json

    # Вход по email
    email_login = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    email_response = test_client.post('/login', json=email_login)
    assert email_response.status_code == 200
    assert "access_token" in email_response.json

    # Вход по телефону
    phone_login = {
        "phone": user_data["phone"],
        "password": user_data["password"]
    }
    phone_response = test_client.post('/login', json=phone_login)
    assert phone_response.status_code == 200
    assert "access_token" in phone_response.json
