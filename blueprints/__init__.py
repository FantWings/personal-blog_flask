from flask import Blueprint
from .bp_archives import archiveAPI
from .bp_auth import authAPI
from .bp_user import userAPI

api_v1 = Blueprint('api', __name__, url_prefix="/v1/")
api_v1.register_blueprint(archiveAPI)
api_v1.register_blueprint(authAPI)
api_v1.register_blueprint(userAPI)
