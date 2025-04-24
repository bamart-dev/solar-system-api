from flask import Blueprint, abort, make_response, request
from app.models.planets import Planet
from app.db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    atmosphere = request_body["atmosphere"]

    new_planet = Planet(
        name=name,
        description=description,
        atmosphere=atmosphere,
        )
    db.session.add(new_planet)
    db.session.commit()

    message = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "atmosphere": new_planet.atmosphere,
    }

    return message, 201


@planets_bp.get("")
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)

    return [
        {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "atmosphere": planet.atmosphere,
        }
    for planet in planets]


# @planets_bp.get("")
# def get_all_planets():
#     results_list = []

#     for planet in planets:
#         results_list.append(dict(
#             id = planet.id,
#             name = planet.name,
#             description = planet.description,
#             atmosphere = planet.atmosphere,
#         ))

#     return results_list

# @planets_bp.get("/<planet_id>")
# def get_one_planet(planet_id):
#     planet = validate_planet(planet_id)

#     return {
#         "id": planet.id,
#         "name": planet.name,
#         "description": planet.description,
#         "atmosphere": planet.atmosphere,
#     }


# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         message = {"mesage": f"planet ({planet_id}) is invalid"}
#         abort(make_response(message, 400))

#     for planet in planets:
#         if planet_id == planet.id:
#             return planet

#     response = {"message": f"planet ({planet_id}) not found"}
#     abort(make_response(response, 404))
