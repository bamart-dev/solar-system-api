from flask import Blueprint, request, make_response, abort, Response
from app.models.planets import Planet
from app.models.systems import System
from app.db import db
from .route_utilities import validate_model

bp = Blueprint("systems_bp", __name__, url_prefix="/systems")


@bp.post("")
def create_system():
    request_body = request.get_json()

    try:
        new_system = System.generate_system(request_body)
    except KeyError as e:
        response = {"message": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_system)
    db.session.commit()

    return make_response(new_system.to_dict(), 201)


@bp.get("")
def get_all_systems():
    query = db.select(System)

    sys_name_param = request.args.get("name")
    if sys_name_param:
        query = query.where(System.name.ilike(f"%{sys_name_param}%"))

    systems = db.session.scalars(query.order_by(System.id))

    return [system.to_dict() for system in systems]


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
    except KeyError as e:
        response = {"message": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))

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
