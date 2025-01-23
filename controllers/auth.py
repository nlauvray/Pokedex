from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from models import db
from models.users import User
from systems.auth import AuthSystem

def get_routes(auth_system: AuthSystem):
    bp = Blueprint('auth', __name__, url_prefix='/auth')

    # Route pour créer un utilisateur
    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # Vérifier si l'utilisateur existe déjà
            existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
            if existing_user:
                flash('Un utilisateur avec cet email existe déjà', 'danger')
                return redirect(url_for('auth.register'))

            # Hacher le mot de passe pour le stockage en base de données
            hashed_password = generate_password_hash(password)

            # Chiffrer le mot de passe avec la clé publique RSA
            encrypted_password = auth_system.encrypt_password(password)

            # Créer un nouvel utilisateur avec le mot de passe chiffré
            new_user = User(username=username, email=email, pwd=encrypted_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Compte créé avec succès', 'success')
            return redirect(url_for('auth.login'))  # Redirige vers la page de connexion

        return render_template('register.html')  # Affiche le formulaire d'inscription

    # Route de connexion
    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username_or_email = request.form['username_or_email']
            password = request.form['password']

            # Vérifier si l'utilisateur existe par email ou par nom d'utilisateur
            user = User.query.filter((User.email == username_or_email) | (User.username == username_or_email)).first()
            
            if user:
                # Déchiffrer le mot de passe avec la clé privée RSA
                decrypted_password = auth_system.decrypt_password(user.pwd)

                # Vérifier le mot de passe avec le mot de passe déchiffré
                if decrypted_password == password:  # Vérification du mot de passe
                    session['user_id'] = user.id
                    flash('Connexion réussie', 'success')
                    return redirect(url_for('pokedex.pokedex'))  # Redirige vers la page du tableau de bord après la connexion
                else:
                    flash('Nom d\'utilisateur, email ou mot de passe incorrect', 'danger')

        return render_template('login.html')  # Affiche le formulaire de connexion

    @bp.route('/logout', methods=['POST'])
    def logout():
        # Supprimer l'ID de l'utilisateur de la session (efface le cookie de session côté client)
        session.pop('user_id', None)
        flash('Vous avez été déconnecté avec succès', 'success')
        return redirect(url_for('auth.login')) 

    @bp.route("/profile", methods=["GET"])
    @AuthSystem.login_required
    def profile():
        user = User.query.get(session['user_id'])
        return render_template("profile.html", user=user)

    return bp
