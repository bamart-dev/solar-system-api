from app import create_app, db
from app.models.planets import  Planet

my_app = create_app()
with my_app.app_context():
    db.session.add(Planet(name="Cat Head Planet", description="cat head shaped planet with large red spots", atmosphere="cat's bathhouse cafe"))
    db.session.add(Planet(name="Donut Planet", description="donut shaped planet with a black hole in the center", atmosphere="non-existant"))
    db.session.add(Planet(name="Jelly Cube", description="perfect pink cube shaped planet with a sugared cherry at the bottom", atmosphere="cannibalistic"))
    db.session.add(Planet(name="Palm Planet", description="shaped like a large etheral palm with its fingers folded upward", atmosphere="surface is a mixtrue of blue and purple gas"))
    db.session.commit()
