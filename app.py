from flask import Flask
from flask_login import LoginManager
from models import db

login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)

from models.user import User
from models.favorite import Favorite

login_manager.init_app(app)
login_manager.login_view = "auth.login"

from routes.auth import auth_bp
from routes.recipe import recipe_bp

app.register_blueprint(auth_bp)
app.register_blueprint(recipe_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)