from flask import Blueprint

print('[INFO] Blueprint Library v1.0 Loaded !')

checkAPI = Blueprint('statusCheck', __name__, url_prefix='/api')
archiveAPI = Blueprint('archive', __name__, url_prefix='/api')
authAPI = Blueprint('auth', __name__, url_prefix='/api')

from . import bp_check, bp_archives