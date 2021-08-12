from flask import Flask
from flask_cors import CORS

from settings import Config
from sql import db

import blueprints

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    db.init_app(app)
    db.create_all()

app.register_blueprint(blueprint=blueprints.checkAPI)
app.register_blueprint(blueprint=blueprints.archiveAPI)

CORS(app, supports_credentials=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)
