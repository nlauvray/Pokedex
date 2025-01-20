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

app = Flask(
    __name__,
    static_folder='./static',
    static_url_path='/static',
    template_folder='./templates'
)
# Fonction pour créer l'application Flask
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Utiliser un fichier config séparé
    
    # Initialisation de la base de données
    db.init_app(app)

    return app

# Créer l'application Flask
app = create_app()

# Chemins pour stocker les clés RSA
PRIVATE_KEY_PATH = 'rsa_private.pem'
PUBLIC_KEY_PATH = 'rsa_public.pem'

# Charger ou générer des clés RSA persistantes
def load_or_generate_rsa_keys():
    if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
        # Charger les clés existantes
        with open(PRIVATE_KEY_PATH, 'rb') as private_file:
            private_key = RSA.import_key(private_file.read())
        with open(PUBLIC_KEY_PATH, 'rb') as public_file:
            public_key = RSA.import_key(public_file.read())
    else:
        # Générer de nouvelles clés
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()
        
        # Sauvegarder les clés dans des fichiers
        with open(PRIVATE_KEY_PATH, 'wb') as private_file:
            private_file.write(private_key.export_key())
        with open(PUBLIC_KEY_PATH, 'wb') as public_file:
            public_file.write(public_key.export_key())

    return private_key, public_key

# Charger les clés RSA au démarrage
private_key, public_key = load_or_generate_rsa_keys()

# Chiffrement du mot de passe avec la clé publique RSA
def encrypt_password_with_public_key(password, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_password = cipher.encrypt(password.encode('utf-8'))
    return base64.b64encode(encrypted_password).decode('utf-8')

# Déchiffrement du mot de passe avec la clé privée RSA
def decrypt_password_with_private_key(encrypted_password, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_password_bytes = base64.b64decode(encrypted_password)
    decrypted_password = cipher.decrypt(encrypted_password_bytes).decode('utf-8')
    return decrypted_password

# Route d'accueil
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
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('Un utilisateur avec cet email existe déjà', 'danger')
            return redirect(url_for('register'))

        # Hacher le mot de passe pour le stockage en base de données
        hashed_password = generate_password_hash(password)

        # Chiffrer le mot de passe avec la clé publique RSA
        encrypted_password = encrypt_password_with_public_key(password, public_key)

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
        username = request.form['username']
        email = request.form['email']  # Nom d'utilisateur ou email
        password = request.form['password']

        # Vérifier si l'utilisateur existe par email ou par nom d'utilisateur
        user = User.query.filter((User.email == email) and (User.username == username)).first()
        
        if user:
            # Déchiffrer le mot de passe avec la clé privée RSA
            decrypted_password = decrypt_password_with_private_key(user.pwd, private_key)

            # Vérifier le mot de passe avec le mot de passe déchiffré
            if decrypted_password == password:  # Vérification du mot de passe
                session['user_id'] = user.id
                flash('Connexion réussie', 'success')
                return redirect(url_for('dashboard'))  # Redirige vers la page du tableau de bord après la connexion
            else:
                flash('Nom d\'utilisateur, email ou mot de passe incorrect', 'danger')

    return render_template('login.html')  # Affiche le formulaire de connexion

# Route protégée - Tableau de bord
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('vous devez être connecté pour accéder au tableau de bord.', 'danger')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/logout', methods=['POST'])
def logout():
    # Supprimer l'ID de l'utilisateur de la session (efface le cookie de session côté client)
    session.pop('user_id', None)
    flash('Vous avez été déconnecté avec succès', 'success')
    return redirect(url_for('home')) 

# Créer la base de données au début + crée toutes les tables nécessaires dans la base de données
with app.app_context():
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True)  # Activation du mode debug pour le développement
