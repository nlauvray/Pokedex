from flask import Blueprint, render_template
from models.pokemon import Pokemon
from infrastructure.pokeapi import PokeApiClient
import jsonpickle

def get_pokemon_routes(pokeApi: PokeApiClient):
    bp = Blueprint('pokemon', __name__)

    @bp.route('/pokemon/<id>')
    def pokemon(id):
        pokemon_data = Pokemon.get_from_api(pokeApi, id)
        pokemon_details = pokeApi.get_pokemon(id)

        return render_template('pokemon.html', pokemon=pokemon_data, details=pokemon_details)

    @bp.route('/api/pokemon/<id>')
    def pokemon_api(id):
        pokemon_data = Pokemon.get_from_api(pokeApi, id)
        return jsonpickle.encode(pokemon_data)

    return bp
