from flask import Blueprint, render_template, request
from models.pokemon import Pokemon
from infrastructure.pokeapi import PokeApiClient
import jsonpickle

def get_routes(poke_api: PokeApiClient):
    bp = Blueprint('pokedex', __name__)

    # Route principale du Pokédex
    @bp.route('/')
    def pokedex():
        return render_template('index.html')

    # Route pour afficher les détails d'un Pokémon
    @bp.route('/pokemon/<int:id>')
    def pokemon(id):
        pokemon = Pokemon.get_from_api(poke_api, id)
        return render_template('pokemon.html', pokemon=pokemon)

    # Route pour la recherche d'un Pokémon
    @bp.route('/search', methods=['GET'])
    def search():
        query = request.args.get('query', '').strip().lower()
        page = request.args.get('page', 1, type=int)
        count, pokemons = Pokemon.search_from_api(poke_api, query, offset=(page - 1) * 20)

        return jsonpickle.encode({
            'pokemons': pokemons,
            'max_page': count // 20
        })

    return bp
