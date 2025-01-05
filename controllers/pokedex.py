from flask import Blueprint, render_template
from models.pokemon import Pokemon
from infrastructure.pokeapi import PokeApiClient

def get_routes():
    bp = Blueprint('pokedex', __name__)
    pokeApi = PokeApiClient('https://pokeapi.co/api/v2')

    @bp.route('/')
    def pokedex():
        pokemons = Pokemon.list_from_api(pokeApi)
        return render_template('index.html', pokemons=pokemons)

    return bp
