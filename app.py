from flask import Flask
from flask_cors import CORS
from settings import FlaskConfig
from sql import db
from blueprints import api_v1


def create_app():
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)
    CORS(app, supports_credentials=True)

    app.register_blueprint(blueprint=api_v1)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
