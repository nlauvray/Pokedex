from flask import Flask, render_template
from controllers.pokemon_fight_api import get_pokemon_fight_routes
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

app = Flask(__name__)
app.config['DEBUG'] = True

app.register_blueprint(get_pokemon_fight_routes(), url_prefix='/fight')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/battle/start', methods=['POST'])
def start_battle():
    # Logique pour démarrer le combat
    return "Battle started!"

if __name__ == "__main__":
    app.run(debug=True)