from flask import Blueprint

def get_routes():
    bp = Blueprint('fight', __name__, url_prefix='/fight')

    @bp.route('/')
    def index():
        return "I'm a teapot", 418

    return bp
