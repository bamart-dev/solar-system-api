from app.db import db
from app.models.systems import System


def test_get_one_system(client, create_system):
    response = client.get("/systems/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Solar System",
        "planets": None,
    }


def test_create_one_system(client):
    response = client.post("/systems", json={"name": "Solar System"})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Solar System",
        "planets": None,
    }


def test_create_one_system_missing_name(client):
    response = client.post("/systems", json={})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "Invalid request: missing name"}


def test_create_one_system_no_data(client):
    response = client.get("/systems/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "system (1) not found"}


def test_create_one_system_invalid_data(client):
    response = client.get("/systems/%&*")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "system (%&*) is invalid"}


def test_get_all_systems(client, create_two_systems):
    response = client.get("/systems")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Solar System",
            "planets": None,
        },
        {
            "id": 2,
            "name": "Alpha Centauri",
            "planets": None,
        },
    ]


def test_get_all_systems_no_data(client):
    response = client.get("/systems")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_update_system(client, create_two_systems):
    response = client.put("/systems/1", json={
        "name": "Lunar System"
    })
    query = db.select(System).where(System.id == 1)
    updated_system = db.session.scalar(query)

    assert response.status_code == 204
    assert updated_system.name == "Lunar System"


def test_update_system_missing_system(client):
    response = client.put("/systems/1", json={
        "name": "Lunar System",
    })
    request_body = response.get_json()

    assert response.status_code == 404
    assert request_body == {"message": "system (1) not found"}


def test_update_system_invalid_id(client, create_two_systems):
    response = client.put("/systems/@", json={
        "name": "Lunar System",
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "message": "system (@) is invalid",
    }


def test_delete_system(client, create_two_systems):
    response = client.delete("/systems/1")

    query = db.select(System).where(System.id == 1)
    deleted_system = db.session.scalar(query)

    assert response.status_code == 204
    assert not deleted_system


def test_delete_planet_missing_planet(client):
    response = client.delete("/systems/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "system (1) not found",
    }


def test_delete_planet_invalid_id(client, create_two_systems):
    response = client.delete("/systems/eight@")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "message": "system (eight@) is invalid",
    }
