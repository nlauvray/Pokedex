from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.model_pokemon import Pokemon, Move
from models.team_Pokemon import TeamPokemon
from models.model_combat import Battle, BattleLog
from models.users import User
from models.teams import Team

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Utiliser un fichier config séparé

    # Initialisation de la base de données
    db.init_app(app)

    return app

app = create_app()


def before_first_request():
    print("Routes enregistrées :")
    for rule in app.url_map.iter_rules():
        print(rule)

# Route d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour afficher tous les Pokémon
# @app.route('/pokemons')
# def pokemons():
#     all_pokemons = Pokemon.query.all()  # Récupère tous les Pokémon de la base de données
#     return render_template('pokemons.html', pokemons=all_pokemons)  # Affiche les Pokémon dans un template

# Route pour afficher un Pokémon spécifique
# @app.route('/pokemon/<int:id>')
# def pokemon(id):
#     pokemon = Pokemon.query.get_or_404(id)  # Récupère le Pokémon avec cet ID
#     return render_template('pokemon_detail.html', pokemon=pokemon)  # Affiche le détail du Pokémon

# Route pour créer un utilisateur
@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Route /register a été atteinte")
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(email=email).first()  # Vérifie si un utilisateur avec cet email existe
        if existing_user:
            flash('Un utilisateur avec cet email existe déjà', 'danger')
            return redirect(url_for('register'))

        # Hachage du mot de passe avant de l'enregistrer
        hashed_password = generate_password_hash(password)

        # Créer un nouvel utilisateur
        new_user = User(username=username, email=email, pwd=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Compte créé avec succès', 'success')
        return redirect(url_for('login'))  # Redirige vers la page de connexion

    return render_template('register.html')  # Affiche le formulaire d'inscription

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Vérifier si l'utilisateur existe
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.pwd, password):  # Vérification du mot de passe
            session['user_id'] = user.id
            flash('Connexion réussie', 'success')
            return redirect(url_for('dashboard'))  # Redirige vers la page du tableau de bord après la connexion
        else:
            flash('Email ou mot de passe incorrect', 'danger')

    return render_template('login.html')  # Affiche le formulaire de connexion

# Route protégée - Tableau de bord
@app.route('/dashboard')
def dashboard():
     if 'user_id' not in session:
         flash('vous devez être connecté pour accéder au tableau de bord.', 'danger')
         return redirect(url_for('login'))
     user = User.query.get(session['user_id'])
     return render_template('dashboard.html', user=user) # Affiche la page du tableau de bord

@app.route('/logout', methods= ['POST'])
def logout():
    # Supprimer l'ID de l'utilisateur de la session (cela efface le cookie de session côté client)
    session.pop('user_id', None)
    flash('Vous avez été déconnecté avec succès', 'success')
    return redirect(url_for('home'))  # Redirige vers la page d'accueil après la déconnexion

# Si tu veux créer la base de données au début
with app.app_context():
    db.create_all()  # Crée toutes les tables nécessaires dans la base de données
    # Vous pouvez vérifier ici si la base de données existe déjà ou si vous devez la recréer.

if __name__ == '__main__':
    app.run(debug=True)  # Activation du mode debug pour le développement
