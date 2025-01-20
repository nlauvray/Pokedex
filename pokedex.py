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

if __name__ == "__main__":
    app.run(debug=True)