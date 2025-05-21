from app.db import db
from app.models.planets import Planet


def test_get_one_planet(client, create_two_planets):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Tatooine",
        "description": "A harsh desert world orbiting twin suns",
        "atmosphere": "Dry; suffers from minor scum and villany problems",
    }


def test_get_one_planet_no_data(client):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "planet (1) not found",
    }


def test_get_one_planet_invalid_data(client):
    response = client.get("/planets/%^&")
    resonse_body = response.get_json()

    assert response.status_code == 400
    assert resonse_body == {
        "message": "planet (%^&) is invalid",
    }


def test_get_all_planets(client, replicate_development_db):
    response = client.get("/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Cat Head Planet",
            "description": "cat head shaped planet with large red spots",
            "atmosphere": "cat's bathhouse cafe",
            },
        {
            "id": 2,
            "name": "Donut Planet",
            "description": "donut shaped planet with a black hole in the center",
            "atmosphere": "non-existant",
            },
        {
            "id": 3,
            "name": "Jelly Cube",
            "description": "perfect pink cube shaped planet with a sugared cherry at the bottom",
            "atmosphere": "cannibalistic",
            },
        {
            "id": 4,
            "name": "Palm Planet",
            "description": "shaped like a large etheral palm with its fingers folded upward",
            "atmosphere": "surface is a mixtrue of blue and purple gas",
            },
    ]


def test_get_all_planets_no_data(client):
    response = client.get("/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_create_one_planet(client):
    response = client.post("/planets", json={
        "name": "Coruscant",
        "description": "A city-covered planet; capital of a galaxy",
        "atmosphere": "Vibrant, very loud",
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Coruscant",
        "description": "A city-covered planet; capital of a galaxy",
        "atmosphere": "Vibrant, very loud",
    }


def test_update_planet(client, create_two_planets):
    response = client.put("/planets/1", json={
        "name": "Dagobah",
        "description": "remote world full of swamps and forests",
        "atmosphere": "pure",
    })
    query = db.select(Planet).where(Planet.id == 1)
    updated_planet = db.session.scalar(query)

    assert response.status_code == 204
    assert updated_planet.name == "Dagobah"
    assert updated_planet.description == "remote world full of swamps and forests"
    assert updated_planet.atmosphere == "pure"


def test_update_planet_missing_planet(client):
    response = client.put("/planets/1", json={
        "name": "Dagobah",
        "description": "remote world full of swamps and forests",
        "atmosphere": "pure",
    })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "planet (1) not found",
    }


def test_update_planet_invalid_id(client, create_two_planets):
    response = client.put("/planets/!", json={
        "name": "Dagobah",
        "description": "remote world full of swamps and forests",
        "atmosphere": "pure",
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "message": "planet (!) is invalid",
    }


def test_delete_planet(client, create_two_planets):
    response = client.delete("/planets/1")

    query = db.select(Planet).where(Planet.id == 1)
    deleted_planet = db.session.scalar(query)

    assert response.status_code == 204
    assert not deleted_planet


def test_delete_planet_missing_planet(client):
    response = client.delete("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "planet (1) not found",
    }


def test_delete_planet_invalid_id(client, create_two_planets):
    response = client.delete("/planets/three")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "message": "planet (three) is invalid",
    }
