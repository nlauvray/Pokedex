from flask import Blueprint, render_template

def get_routes():
    bp = Blueprint('pokedex', __name__)

    @bp.route('/')
    def pokedex():
        return render_template('index.html')

    return bp
