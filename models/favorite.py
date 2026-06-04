from . import db

class Favorite(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    recipe_id = db.Column(
        db.String(100),
        nullable=False
    )

    recipe_name = db.Column(
        db.String(255),
        nullable=False
    )

    recipe_image = db.Column(
        db.String(500)
    )