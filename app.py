from connexion import FlaskApp
import os
from config import connex_app


connex_app.add_api('openapi.yaml')


if __name__ == "__main__":
    connex_app.run(host='0.0.0.0', debug=True)