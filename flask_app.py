import secrets
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin
from flask_login import login_user, current_user, logout_user, login_required
import base64
from PIL import Image

app = Flask(__name__)
app.secret_key = 'soujgpoisefpowigmppwoigvhw0wefwefwogihj'

# Configuration for database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"

# Initialize database with Flask app
db.init_app(app) # ????? HOW TO IMPORT??


# code lmao

if __name__ == "__main__":
    app.secret_key = "super_secret_key"  # Change this to a random, secure key
    app.run(debug=True)