from flask import Blueprint, abort, make_response
from app.models.planets import planets

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.get("")
def get_all_planets():
    results_list = []

    for planet in planets:
        results_list.append(dict(
            id = planet.id,
            name = planet.name,
            description = planet.description,
            atmosphere = planet.atmosphere,
        ))

    return results_list

@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        return {"message": f"planet ({planet_id}) is invalid"}, 400

    for planet in planets:
        if planet_id == planet.id:
            return {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "atmosphere": planet.atmosphere,
            }

    # return {"message": f"planet ({planet_id}) not found"}, 404
    response = {"message": f"planet ({planet_id}) not found"}
    abort(make_response(response, 404))
