from flask import Blueprint, render_template, request, jsonify, session
from infrastructure.pokeapi import PokeApiClient
from fight.battle_manager import BattlePokemon, BattleManager
import random

def get_pokemon_fight_routes(pokeApi):
    pokeApi = PokeApiClient ('https://pokeapi.co/api/v2')
    bp = Blueprint('pokefight', __name__)

    @bp.route('/fight')
    def pokefight():
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
        
        return render_template('fight.html', abilities=abilities, types=types, stats=stats, attacks=attacks, speAttacks=speAttacks, categories=categories, conditions=conditions, natures=natures, items=items, berries=berries)

    @bp.route('/start_battle', methods=['POST'])
    def start_battle():
        print(request.json)
        player_team = request.json.get('player_team')
        if not player_team or len(player_team) < 3 or len(player_team) > 5:
            # return jsonify({"error": "Player team must contain between 3 and 5 Pokémon"}), 400
            pass

        opponent_team = generate_random_team(pokeApi, len(player_team))

        player_pokemons = [BattlePokemon.from_api_data(pokeApi.get_pokemon(f'{pokemon}')) for pokemon in player_team]
        opponent_pokemons = [BattlePokemon.from_api_data(pokeApi.get_pokemon(f'{pokemon}')) for pokemon in opponent_team]

        battle_manager = BattleManager(player_pokemons, opponent_pokemons)
        session['battle_manager'] = battle_manager
        print(session)
        return jsonify({"message": "Battle started!", "opponent_team": opponent_team})

    @bp.route('/battle_turn', methods=['POST'])
    def battle_turn():
        print(session.keys())
        move_name = request.json['move']
        battle_manager = session.get('battle_manager')
        player_move = next(move for move in battle_manager.player_pokemon.moves if move.name == move_name)
        result = battle_manager.battle_turn(player_move)
        return jsonify({"result": result})

    def generate_random_team(pokeApi, team_size):
        all_pokemon = pokeApi.get_pokemon('?limit=1000&offset=0')
        return random.sample([pokemon for pokemon in all_pokemon], team_size)

    return bp
    # pokeAbility = PokeApiClient('https://pokeapi.co/api/v2/ability?limit=100000&offset=0')
    # pokeType = PokeApiClient('https://pokeapi.co/api/v2/type?limit=100000&offset=0')
    # pokeStat = PokeApiClient('https://pokeapi.co/api/v2/stat?limit=100000&offset=0')
    # pokeAttack = PokeApiClient('https://pokeapi.co/api/v2/move?limit=100000&offset=0')
    # pokeSpeAttack = PokeApiClient('https://pokeapi.co/api/v2/move-damage-class?limit=100000&offset=0')
    # pokeCategory = PokeApiClient('https://pokeapi.co/api/v2/move-category?limit=100000&offset=0')
    # pokeCondition = PokeApiClient('https://pokeapi.co/api/v2/encounter-condition?limit=100000&offset=0')
    # pokeNature = PokeApiClient('https://pokeapi.co/api/v2/nature?limit=100000&offset=0')
    # pokeItem = PokeApiClient('https://pokeapi.co/api/v2/item?limit=100000&offset=0')
    # pokeBerry = PokeApiClient('https://pokeapi.co/api/v2/berry?limit=100000&offset=0')