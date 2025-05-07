from flask import Blueprint, abort, make_response, request, Response
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
    query = db.select(Planet)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(
            Planet.description.ilike(f"%{description_param}%"))

    atmosphere_param = request.args.get("atmosphere")
    if atmosphere_param:
        query = query.where(
            Planet.atmosphere.ilike(f"%{atmosphere_param}%"))

    query = query.order_by(Planet.id)
    planets = db.session.scalars(query)

    return [
        {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "atmosphere": planet.atmosphere,
        }
    for planet in planets]


@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "atmosphere": planet.atmosphere,
    }


@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.atmosphere = request_body["atmosphere"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        message = {"message": f"planet ({planet_id}) is invalid"}
        abort(make_response(message, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)

    if not planet:
        response = {"message": f"planet ({planet_id}) not found"}
        abort(make_response(response, 404))

    return planet
