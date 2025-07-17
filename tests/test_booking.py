def test_create_booking(test_client, booking_data, auth_header):
    response = test_client.post('/api/bookings', json=booking_data, headers=auth_header)
    print("Create booking response status:", response.status_code)
    print("Create booking response json:", response.json)
    assert response.status_code == 201
    data = response.json
    assert "id" in data
    assert data["room_id"] == booking_data["room_id"]
    assert data["check_in"] == booking_data["check_in"]
    assert data["check_out"] == booking_data["check_out"]


def test_get_booking(test_client, booking_data, auth_header):
    create_resp = test_client.post('/api/bookings', json=booking_data, headers=auth_header)
    booking_id = create_resp.json["id"]

    resp = test_client.get(f'/api/bookings/{booking_id}', headers=auth_header)
    assert resp.status_code == 200
    data = resp.json
    assert data["id"] == booking_id


def test_update_booking(test_client, booking_data, auth_header):
    create_resp = test_client.post('/api/bookings', json=booking_data, headers=auth_header)
    booking_id = create_resp.json["id"]

    resp = test_client.put(
        f'/api/bookings/{booking_id}',
        json={"guests": 5, "notes": "Обновлено"},
        headers=auth_header
    )
    assert resp.status_code == 200
    data = resp.json
    assert data["guests"] == 5


def test_delete_booking(test_client, booking_data, auth_header):
    create_resp = test_client.post('/api/bookings', json=booking_data, headers=auth_header)
    booking_id = create_resp.json["id"]

    resp = test_client.delete(f'/api/bookings/{booking_id}', headers=auth_header)
    assert resp.status_code == 204

    resp2 = test_client.get(f'/api/bookings/{booking_id}', headers=auth_header)
    assert resp2.status_code == 404
