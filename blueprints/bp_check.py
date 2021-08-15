from flask import make_response
from . import checkAPI
from utils.log import log

log("Loaded CheckAPI. [Ver 1.0]")


@checkAPI.route("/check")
def service_check():
    return make_response({"status": "ok"})
