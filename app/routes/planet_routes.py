from flask import Blueprint, abort, make_response, request, Response
from app.models.planets import Planet
from app.db import db
from .route_utilities import (
    validate_model, create_model,
    get_model_with_filters, missing_attribute_error)


bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


@bp.post("")
def create_planet():
    request_body = request.get_json()

    return create_model(Planet, request_body)


@bp.get("")
def get_all_planets():

    return get_model_with_filters(Planet, request.args)

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
