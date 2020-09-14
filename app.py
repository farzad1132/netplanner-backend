from connexion import FlaskApp
import os

app = FlaskApp(__name__, specification_dir='openapi/')

app.add_api('openapi.yaml')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)