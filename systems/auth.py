import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from functools import wraps
from flask import session, flash, redirect, url_for

class AuthSystem:
    private_key: RSA.RsaKey
    public_key: RSA.RsaKey

    # Chemins pour stocker les clés RSA
    PRIVATE_KEY_PATH = 'rsa_private.pem'
    PUBLIC_KEY_PATH = 'rsa_public.pem'

    def __init__(self):
        self.private_key, self.public_key = self.load_or_generate_rsa_keys()
        pass

    # Charger ou générer des clés RSA persistantes
    @staticmethod
    def load_or_generate_rsa_keys():
        if os.path.exists(AuthSystem.PRIVATE_KEY_PATH) and os.path.exists(AuthSystem.PUBLIC_KEY_PATH):
            # Charger les clés existantes
            with open(AuthSystem.PRIVATE_KEY_PATH, 'rb') as private_file:
                private_key = RSA.import_key(private_file.read())
            with open(AuthSystem.PUBLIC_KEY_PATH, 'rb') as public_file:
                public_key = RSA.import_key(public_file.read())
        else:
            # Générer de nouvelles clés
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            
            # Sauvegarder les clés dans des fichiers
            with open(AuthSystem.PRIVATE_KEY_PATH, 'wb') as private_file:
                private_file.write(private_key.export_key())
            with open(AuthSystem.PUBLIC_KEY_PATH, 'wb') as public_file:
                public_file.write(public_key.export_key())

        return private_key, public_key

    # Chiffrement du mot de passe avec la clé publique RSA
    def encrypt_password(self, password: str):
        cipher = PKCS1_OAEP.new(self.public_key)
        encrypted_password = cipher.encrypt(password.encode('utf-8'))
        return base64.b64encode(encrypted_password).decode('utf-8')

    # Déchiffrement du mot de passe avec la clé privée RSA
    def decrypt_password(self, encrypted_password: str):
        cipher = PKCS1_OAEP.new(self.private_key)
        encrypted_password_bytes = base64.b64decode(encrypted_password)
        decrypted_password = cipher.decrypt(encrypted_password_bytes).decode('utf-8')
        return decrypted_password

    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('vous devez être connecté pour accéder à cette page.', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
