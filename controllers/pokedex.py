from flask import Blueprint, jsonify, render_template, request
from models.pokemon import Pokemon
from infrastructure.pokeapi import PokeApiClient

def get_routes(poke_api: PokeApiClient):
    bp = Blueprint('pokedex', __name__)

    # Route principale du Pokédex
    @bp.route('/')
    def pokedex():
        pokemons = Pokemon.list_from_api(poke_api)
        return render_template('index.html', pokemons=pokemons)

    # Route pour afficher les détails d'un Pokémon
    @bp.route('/pokemon/<int:id>')
    def pokemon(id):
        pokemon = Pokemon.get_from_api(poke_api, id)
        return render_template('pokemon.html', pokemon=pokemon)

    # Route pour la recherche d'un Pokémon
    @bp.route('/search', methods=['GET'])
    def search():
        query = request.args.get('query', '').strip().lower()
        pokemons = []

        if query:
            try:
                pokemon_data = poke_api.get_pokemon(query)
                pokemons = [{
                    'name': pokemon_data['name'],
                    'image_url': pokemon_data['sprites']['front_default']
                }]
            except ValueError:
                pokemons = []

        return jsonify(pokemons)

    return bp
