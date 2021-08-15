from flask import Blueprint
from utils.log import log

log('Loaded Blueprint Library. [ver1.0]')

checkAPI = Blueprint('statusCheck', __name__, url_prefix='/api')
archiveAPI = Blueprint('archive', __name__, url_prefix='/api')
authAPI = Blueprint('auth', __name__, url_prefix='/api')

from . import bp_check, bp_archives, bp_auth
