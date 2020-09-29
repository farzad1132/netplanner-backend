import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=os.path.join(basedir, "openapi"))

# Get the underlying Flask app instance
app = connex_app.app

# Build the Sqlite ULR for SqlAlchemy
postgresql_url = 'postgresql://postgres:1234@localhost:5433/netplanner'

# Configure the SqlAlchemy part of the app instance
app.config["SECRET_KEY"] = '61837f3a27abb1e4b88a47d0502cf2e604071378a1e9ec4c42eafbba933180a7'
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = postgresql_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

bcrypt = Bcrypt(app)