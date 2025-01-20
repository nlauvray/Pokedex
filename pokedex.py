from flask import Flask, render_template, request, jsonify, redirect, url_for
from infrastructure.pokeapi import PokeApiClient
from controllers.pokemon_fight_api import get_pokemon_fight_routes
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'BAD_SECRET_KEY'

pokeApi = PokeApiClient('https://pokeapi.co/api/v2')

bp = get_pokemon_fight_routes(pokeApi)
app.register_blueprint(bp, url_prefix='/fight')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def home_redirect():
    return render_template('home.html')

@app.route('/fight', methods=['GET', 'POST'])
def fight():
    if request.method == 'POST':
        player_team = request.form.getlist('player_team')
        if not player_team:
            return jsonify({"error": "No player team provided"}), 400
        return redirect(url_for('pokefight.start_battle', player_team=player_team))
    return render_template('fight.html')

@app.route('/fight/start_battle', methods=['POST'])
def start_battle():
    data = request.get_json()
    player_pokemon = data['player_team'][0]  # Example: Start with the first Pokemon
    opponent_pokemon = data['opponent_team'][0]  # Example: Start with the first opponent Pokemon

    # Mock data
    player_data = {
        'name': player_pokemon,
        'image': f'/static/{player_pokemon}.png',
        'abilities': ['Blaze', 'Solar Power'],
        'types': ['Fire'],
        'stats': 'HP: 39, Attack: 52, Defense: 43',
        'attacks': ['Tackle', 'Ember', 'Leer']
    }
    opponent_data = {
        'name': opponent_pokemon,
        'image': f'/static/{opponent_pokemon}.png',
        'abilities': ['Overgrow'],
        'types': ['Water'],
        'stats': 'HP: 44, Attack: 48, Defense: 65',
        'attacks': ['Tackle', 'Water Gun']
    }

    return jsonify({
        'message': 'Battle started!',
        'player_image': player_data['image'],
        'opponent_image': opponent_data['image'],
        'player_abilities': ', '.join(player_data['abilities']),
        'player_types': ', '.join(player_data['types']),
        'player_stats': player_data['stats'],
        'player_attacks': ', '.join(player_data['attacks']),
        'opponent_abilities': ', '.join(opponent_data['abilities']),
        'opponent_types': ', '.join(opponent_data['types']),
        'opponent_stats': opponent_data['stats'],
        'opponent_attacks': ', '.join(opponent_data['attacks']),
    })

@app.route('/fight/battle_turn', methods=['POST'])
def battle_turn():
    data = request.get_json()
    move = data['move']

    # Mock battle logic
    result = f"{move} used!"

    # Return updated battle state
    return jsonify({
        'result': result,
        'player_stats': 'HP: 30, Attack: 52, Defense: 43',  # Example update
        'opponent_stats': 'HP: 35, Attack: 48, Defense: 65',  # Example update
        'battle_over': False
    })

if __name__ == "__main__":
    app.run(debug=True)