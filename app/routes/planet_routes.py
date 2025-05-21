from flask import Blueprint, abort, make_response, request, Response
from app.models.planets import Planet
from .route_utilities import validate_model, missing_attribute_error
from app.db import db


bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


@bp.post("")
def create_planet():
    request_body = request.get_json()

    try:
        new_planet = Planet.generate_planet(request_body)
    except KeyError as missing:
        missing_attribute_error(missing)

    db.session.add(new_planet)
    db.session.commit()

    return make_response(new_planet.to_dict(), 201)


@bp.get("")
def get_all_planets():
    query = db.select(Planet)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    atmosphere_param = request.args.get("atmosphere")
    if atmosphere_param:
        query = query.where(Planet.atmosphere.ilike(f"%{atmosphere_param}%"))

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


@bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    return planet.to_dict()


@bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    try:
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.atmosphere = request_body["atmosphere"]
    except KeyError as missing:
        missing_attribute_error(missing)

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
