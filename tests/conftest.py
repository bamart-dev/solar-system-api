import pytest
from app import create_app
from app.db import db
from app.models.planets import Planet
from flask.signals import request_finished
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get(
            'SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def create_two_planets(app):
    tatooine = Planet(
        name="Tatooine",
        description="A harsh desert world orbiting twin suns",
        atmosphere="Dry; suffers from minor scum and villany problems")
    coruscant = Planet(
        name="Coruscant",
        description="A city-covered planet; capital of a galaxy",
        atmosphere="Vibrant, very loud")

    db.session.add_all([tatooine, coruscant])
    db.session.commit()


@pytest.fixture
def replicate_development_db(app):
    chp = Planet(
        name="Cat Head Planet",
        description="cat head shaped planet with large red spots",
        atmosphere="cat's bathhouse cafe",
        )
    dp = Planet(
        name="Donut Planet",
        description="donut shaped planet with a black hole in the center",
        atmosphere="non-existant")
    jc = Planet(
        name="Jelly Cube",
        description="perfect pink cube shaped planet with a sugared cherry at the bottom",
        atmosphere="cannibalistic")
    pp = Planet(
        name="Palm Planet",
        description="shaped like a large etheral palm with its fingers folded upward",
        atmosphere="surface is a mixtrue of blue and purple gas")

    db.session.add_all([chp, dp, jc, pp])
    db.session.commit()
