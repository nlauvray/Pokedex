from flask import Blueprint, render_template, request, session, redirect, url_for
from infrastructure.pokeapi import PokeApiClient
from systems.fight import FightSystem
import random
import jsonpickle

def get_routes(pokeApi: PokeApiClient, fightSystem: FightSystem):
    pokeApi = PokeApiClient('https://pokeapi.co/api/v2')
    bp = Blueprint('fight', __name__, url_prefix='/fight')

    @bp.route('/wip')
    def wip():
        return render_template('fight-wip.html')

    @bp.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            player_team = request.form.getlist('player_team')
            if not player_team or len(player_team) < 3 or len(player_team) > 5:
                player_team = generate_random_team(pokeApi, 3)  # Générer une équipe aléatoire de 3 Pokémon

            opponent_team = generate_random_team(pokeApi, len(player_team))

            fight = fightSystem.start_fight(player_team, opponent_team)
            session['battle_manager_data'] = {
                'fight_id': fight.id,
                'current_player': 1,
            }
            return render_template('fight.html', battle_manager=battle_manager)

        fight_id = session.get('fight_id')
        if fight_id:
            fight = Fight.get(fight_id)
            player_pokemons = [Pokemon.get_from_api(pokeApi, pokemon) for pokemon in fight.team1.pokemons]
            opponent_pokemons = [Pokemon.get_from_api(pokeApi, pokemon) for pokemon in fight.team2.pokemons]

        return render_template('fight.html')

    @bp.route('/battle_turn', methods=['POST'])
    def battle_turn():
        move_name = request.form['move']
        fight_id = session.get('fight_id')
        current_player = session.get('current_player')
        if not fight_id or not current_player:
            return redirect(url_for('fight.index'))

        fight = Fight.get(fight_id)
        new_hp = battle_manager.turn(fight, current_player, move_name)

        if type(new_hp) == bool:
            return jsonpickle.encode({'error': 'Current pokemon has fainted, choose another'}), 400

        if new_hp != 0:
            session['current_player'] = 1 if current_player == 2 else 2

        return jsonpickle.encode({'current_player': session.get('current_player'), 'new_hp': new_hp})

    @bp.route('/change_pokemon', methods=['POST'])
    def change_pokemon():
        slot = request.form['slot']
        fight_id = session.get('fight_id')
        current_player = session.get('current_player')
        if not fight_id or not current_player:
            return redirect(url_for('fight.index'))

        fight = Fight.get(fight_id)
        done = battle_manager.change_pokemon(fight, current_player, slot)

        session['current_player'] = 1 if current_player == 2 else 2

        if not done:
            return jsonpickle.encode({'error': 'Choosen pokemon has fainted'}), 400

        return jsonpickle.encode({'current_player': session.get('current_player')})

    def generate_random_team(pokeApi, team_size):
        all_pokemon = pokeApi.get_pokemons(limit=-1)["result"]
        return random.sample([pokemon['name'] for pokemon in all_pokemon], team_size)

    return bp
