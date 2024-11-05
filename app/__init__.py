from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_socketio import SocketIO
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login'  # Redirect to login page if not authenticated
login_manager.login_message = "Please log in to access this page."  # Optional: custom login message
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)

    # Import and register blueprints after initialization to avoid circular imports
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)




    return app

# Define user_loader for Flask-Login to retrieve the logged-in user by ID
@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Import the User model
    return User.query.get(int(user_id))  # Return the user object based on the user ID stored in the session
