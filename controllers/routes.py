from flask import Blueprint, jsonify, render_template, request
from models.pokemon import Pokemon
from infrastructure.pokeapi import PokeApiClient

def get_routes():
    bp = Blueprint('pokedex', __name__)
    pokeApi = PokeApiClient('https://pokeapi.co/api/v2')

    # Route principale du Pokédex
    @bp.route('/')
    def pokedex():
        pokemons = Pokemon.list_from_api(pokeApi)
        return render_template('index.html', pokemons=pokemons)

    # Route pour afficher les détails d'un Pokémon
    @bp.route('/pokemon/<id>')
    def pokemon(id):
        pokemon_data = Pokemon.get_from_api(pokeApi, id)
        pokemon_details = pokeApi.get_pokemon(id)
        return render_template('pokemon.html', pokemon=pokemon_data, details=pokemon_details)

    # Route pour la recherche d'un Pokémon
    @bp.route('/search', methods=['GET'])
    def search_pokemon():
        query = request.args.get('query', '').strip().lower()
        pokemons = []

        if query:
            try:
                pokemon_data = pokeApi.get_pokemon(query)
                pokemons = [{
                    'name': pokemon_data['name'],
                    'image_url': pokemon_data['sprites']['front_default']
                }]
            except ValueError:
                pokemons = []

        return jsonify(pokemons)

    return bp
