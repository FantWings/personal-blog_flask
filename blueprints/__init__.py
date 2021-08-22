from flask import Blueprint
from utils.log import log

log("Loaded Blueprint Library. [ver1.0]")

checkAPI = Blueprint("statusCheck", __name__, url_prefix="/v1/api")
archiveAPI = Blueprint("archive", __name__, url_prefix="/api/v1/archive")
authAPI = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
userAPI = Blueprint("user", __name__, url_prefix="/api/v1/user")

from . import bp_check, bp_archives, bp_auth, bp_user
