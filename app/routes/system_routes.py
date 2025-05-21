from flask import Blueprint, request, make_response, abort, Response
from app.models.planets import Planet
from app.models.systems import System
from app.db import db
from .route_utilities import (
    validate_model, create_model,
    get_model_with_filters, missing_attribute_error)

bp = Blueprint("systems_bp", __name__, url_prefix="/systems")


@bp.post("")
def create_system():
    request_body = request.get_json()

    return create_model(System, request_body)


@bp.get("")
def get_all_systems():

    return get_model_with_filters(System, request.args)


@bp.get("/<system_id>")
def get_one_system(system_id):
    system = validate_model(System, system_id)

    return system.to_dict()


@bp.put("/<system_id>")
def update_system(system_id):
    system = validate_model(System, system_id)
    request_body = request.get_json()

    try:
        system.name = request_body["name"]
    except KeyError as missing:
        missing_attribute_error(missing)

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<system_id>")
def delete_system(system_id):
    system = validate_model(System, system_id)

    db.session.delete(system)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<system_id>/planets")
def add_planet_to_system(system_id):
    system = validate_model(System, system_id)
    planets = request.get_json()["planet_ids"]
    planet_list = []

    for planet_id in planets:
        planet = validate_model(Planet, planet_id)
        planet.system_id = system_id
        planet_list.append(planet)

    system.planets = planet_list
    db.session.commit()

    return {"id": system.id, "name": system.name, "planets": system.planets}


@bp.get("/<system_id>/planets")
def get_planets_by_system(system_id):
    system = validate_model(System, system_id)

    return [planet.to_dict() for planet in system.planets]
