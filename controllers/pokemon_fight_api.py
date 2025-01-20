from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from infrastructure.pokeapi import PokeApiClient
from fight.battle_manager import BattlePokemon, BattleManager
import random

def get_pokemon_fight_routes(pokeApi):
    pokeApi = PokeApiClient('https://pokeapi.co/api/v2')
    bp = Blueprint('pokefight', __name__)

    @bp.route('/fight', methods=['GET', 'POST'])
    def pokefight():
        if request.method == 'POST':
            player_team = request.form.getlist('player_team')
            if not player_team or len(player_team) < 3 or len(player_team) > 5:
                player_team = generate_random_team(pokeApi, 3)  # Générer une équipe aléatoire de 3 Pokémon

            opponent_team = generate_random_team(pokeApi, len(player_team))

            try:
                player_pokemons = [BattlePokemon.from_api_data(pokeApi.get_pokemon(f'{pokemon}')) for pokemon in player_team]
                opponent_pokemons = [BattlePokemon.from_api_data(pokeApi.get_pokemon(f'{pokemon}')) for pokemon in opponent_team]
            except Exception as e:
                return jsonify({"error": "Error fetching Pokémon data"}), 500

            battle_manager = BattleManager(player_pokemons, opponent_pokemons)
            session['battle_manager_data'] = {
                'player_pokemons': player_team,
                'opponent_pokemons': opponent_team
            }
            return render_template('fight.html', battle_manager=battle_manager)

        abilities = pokeApi.get('ability?limit=100000&offset=0')
        types = pokeApi.get('type?limit=100000&offset=0')
        stats = pokeApi.get('stat?limit=100000&offset=0')
        attacks = pokeApi.get('move?limit=100000&offset=0')
        speAttacks = pokeApi.get('move-damage-class?limit=100000&offset=0')
        categories = pokeApi.get('move-category?limit=100000&offset=0')
        conditions = pokeApi.get('encounter-condition?limit=100000&offset=0')
        natures = pokeApi.get('nature?limit=100000&offset=0')
        items = pokeApi.get('item?limit=100000&offset=0')
        berries = pokeApi.get('berry?limit=100000&offset=0')
        
        battle_manager_data = session.get('battle_manager_data')
        battle_manager = None
        if battle_manager_data:
            player_pokemons = [BattlePokemon.from_api_data(pokeApi.get_pokemon(f'{pokemon}')) for pokemon in battle_manager_data['player_pokemons']]
            opponent_pokemons = [BattlePokemon.from_api_data(pokeApi.get_pokemon(f'{pokemon}')) for pokemon in battle_manager_data['opponent_pokemons']]
            battle_manager = BattleManager(player_pokemons, opponent_pokemons)
        
        return render_template('fight.html', abilities=abilities, types=types, stats=stats, attacks=attacks, speAttacks=speAttacks, categories=categories, conditions=conditions, natures=natures, items=items, berries=berries, battle_manager=battle_manager)

    @bp.route('/battle_turn', methods=['POST'])
    def battle_turn():
        move_name = request.form['move']
        battle_manager_data = session.get('battle_manager_data')
        
        player_pokemons = [BattlePokemon.from_api_data(pokeApi.get_pokemon(f'{pokemon}')) for pokemon in battle_manager_data['player_pokemons']]
        opponent_pokemons = [BattlePokemon.from_api_data(pokeApi.get_pokemon(f'{pokemon}')) for pokemon in battle_manager_data['opponent_pokemons']]
        battle_manager = BattleManager(player_pokemons, opponent_pokemons)
        
        player_move = next(move for move in battle_manager.player_pokemon.moves if move.name == move_name)
        result = battle_manager.battle_turn(player_move)
        
        session['battle_manager_data'] = {
            'player_pokemons': battle_manager_data['player_pokemons'],
            'opponent_pokemons': battle_manager_data['opponent_pokemons']
        }
        
        return render_template('fight.html', battle_manager=battle_manager, result=result)

    def generate_random_team(pokeApi, team_size):
        all_pokemon = pokeApi.get('pokemon?limit=1000&offset=0')['results']
        return random.sample([pokemon['name'] for pokemon in all_pokemon], team_size)

    return bp