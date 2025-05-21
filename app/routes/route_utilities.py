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


def missing_attribute_error(missing):
    response = {"message": f"Invalid request: missing {missing.args[0]}"}
    abort(make_response(response, 400))


def create_model(cls, model_data):
    try:
        new_model = cls.generate_from_dict(model_data)
    except KeyError as missing:
        missing_attribute_error(missing)

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201


def get_model_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(
                    getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))

    return [model.to_dict() for model in models]
