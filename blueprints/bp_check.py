from flask import make_response
from . import checkAPI
from utils.log import log

log('Blueprint - checkAPI Loaded.')


@checkAPI.route('/check')
def service_check():
    return make_response({'status': 'ok'})
