from flask import Blueprint, jsonify, request
from services.pokemon_services import PokemonApiService
from fight.battle_manager import BattleManager
from flask import render_template

def get_pokemon_fight_routes():
    bp = Blueprint('pokefight', __name__)
    
    # Créer une seule instance du service
    pokemon_service = PokemonApiService()
    battle_manager = BattleManager(pokemon_service)

    @bp.route('/api/battle/start', methods=['POST'])
    def start_battle():
        data = request.get_json()
        try:
            battle_state = battle_manager.initialize_battle(
                data['player_pokemon_id'],
                data['opponent_pokemon_id']
            )
            return jsonify({
                'status': 'success',
                'data': battle_state
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400

    @bp.route('/fight')
    def pokefight():
        # Récupérer la liste des Pokémon disponibles
        pokemons = pokemon_service.api_clients['pokemon'].get_pokemons(limit=151)
        return render_template('selectTeam.html', pokemons=pokemons)

    @bp.route('/api/battle/turn', methods=['POST'])
    def execute_turn():
        data = request.get_json()
        try:
            battle_state = battle_manager.execute_turn(data['move_index'])
            return jsonify({
                'status': 'success',
                'data': battle_state
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
            
    @bp.route('/api/pokemon')
    def get_pokemon_list():
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        try:
            pokemon_list = pokemon_service.api_clients['pokemon'].get_pokemons(
                limit=limit,
                offset=offset
            )
            return jsonify({
                'status': 'success',
                'data': pokemon_list
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400

    return bp
