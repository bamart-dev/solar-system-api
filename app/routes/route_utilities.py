from flask import abort, make_response
from app.db import db


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        message = {
            "message": f"{cls.__name__.lower()} ({model_id}) is invalid",
            }
        abort(make_response(message, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {
            "message": f"{cls.__name__.lower()} ({model_id}) not found",
            }
        abort(make_response(response, 404))

    return model
