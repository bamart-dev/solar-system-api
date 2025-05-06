

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
