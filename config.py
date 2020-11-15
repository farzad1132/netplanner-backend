import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

# This handler will respond to exceptions that connexion does not cover it.
# for example connexion is handling BadRequest but its not handling TypeError which this handler comes into play
# here we are not specifying any status code because a variety of exceptions may invoke this handler and
#  it's just for informing the client
def general_exception_handler(e):
    return {"error_msg": e.__str__()}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__,
                            specification_dir=os.path.join(BASE_DIR, "openapi"))

connex_app.add_error_handler(Exception, general_exception_handler)

# Get the underlying Flask app instance
app = connex_app.app
DB = os.environ["DB"]
DB_PORT = os.environ["DB_PORT"]
DB_HOST = os.environ["DB_HOST"]
DB_PASS = os.environ["DB_PASS"]
DB_USER = os.environ["DB_USER"]
db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB}"


# Configure the SqlAlchemy part of the app instance
app.config["SECRET_KEY"] = '61837f3a27abb1e4b88a47d0502cf2e604071378a1e9ec4c42eafbba933180a7'
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

bcrypt = Bcrypt(app)