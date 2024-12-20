from flask import Blueprint, render_template
from models.pokemon import Pokemon
from infrastructure.pokeapi import PokeApiClient

def get_routes(pokeApi: PokeApiClient):
    bp = Blueprint('pokemon', __name__)

    @bp.route('/pokemon/<id>')
    def pokemon(id):
        return render_template('pokemon.html', pokemon=Pokemon.get_from_api(pokeApi, id))

    return bp
