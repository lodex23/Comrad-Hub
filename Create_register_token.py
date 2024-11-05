from app import db, create_app  # Import your app creation function
from app.models import RegistrationToken
import secrets

app = create_app()  # Create an instance of your Flask app

# Use the application context
with app.app_context():
    token = RegistrationToken(token=secrets.token_hex(32))
    db.session.add(token)
    db.session.commit()
    print(f"Generated token: {token.token}")
