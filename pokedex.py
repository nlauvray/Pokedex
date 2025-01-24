from flask import Flask, render_template
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.model_pokemon import Pokemon, Move
from models.team_Pokemon import TeamPokemon
from models.model_combat import Battle, BattleLog
from models.users import User
from models.teams import Team
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

from controllers import auth, teams, pokedex, fight

from systems.auth import AuthSystem
from infrastructure.pokeapi import PokeApiClient

app = Flask(
    __name__,
    static_folder='./static',
    static_url_path='/static',
    template_folder='./templates'
)

app.config.from_object('config.Config')  # Utiliser un fichier config séparé

# Initialisation de la base de données
db.init_app(app)

# Systems
auth_system = AuthSystem()
pokeapi_client = PokeApiClient("https://pokeapi.co/api/v2")

# Blueprints
app.register_blueprint(auth.get_routes(auth_system))
app.register_blueprint(teams.get_routes())
app.register_blueprint(pokedex.get_routes(pokeapi_client))
app.register_blueprint(fight.get_routes())

# Créer la base de données au début + crée toutes les tables nécessaires dans la base de données
with app.app_context():
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True)  # Activation du mode debug pour le développement
