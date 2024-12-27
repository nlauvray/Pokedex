from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
generate_password_hash, check_password_hash
from models import db
from models.model_pokemon import Pokemon, Move
from models.team_Pokemon import TeamPokemon
from models.model_combat import Battle, BattleLog
from models.users import User
from models.teams import Team
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64

# Fonction pour générer les clés RSA
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Fonction pour chiffrer des données avec RSA
def encrypt_with_rsa(data, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted_data = cipher.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypted_data).decode('utf-8')

# Fonction pour déchiffrer des données avec RSA
def decrypt_with_rsa(encrypted_data, private_key):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))
    return decrypted_data.decode('utf-8')

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Utiliser un fichier config séparé

    # Initialisation de la base de données
    db.init_app(app)

    return app

app = create_app()

#Route d'acceuil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour créer un utilisateur
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Un utilisateur avec cet email existe déjà', 'danger')
            return redirect(url_for('register'))

        # Hachage du mot de passe avant de l'enregistrer
        hashed_password = generate_password_hash(password)

        # Chiffrement du mot de passe avec RSA pour une sécurité supplémentaire
        private_key, public_key = generate_rsa_keys()
        encrypted_password = encrypt_with_rsa(hashed_password, public_key)

        # Créer un nouvel utilisateur avec le mot de passe chiffré
        new_user = User(username=username, email=email, pwd=encrypted_password)
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
        if user:
            # Déchiffrer le mot de passe avec RSA
            private_key, public_key = generate_rsa_keys()  # Utiliser la clé privée associée
            decrypted_password = decrypt_with_rsa(user.pwd, private_key)

            if check_password_hash(decrypted_password, password):  # Vérification du mot de passe
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

if __name__ == '__main__':
    app.run(debug=True)  # Activation du mode debug pour le développement
