# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pokedex.db'  # URI de la base de données
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactive la modification des signaux, il est fortement conseillé de laisser cette option par défaut.
    SECRET_KEY = 'supersecretkey'  # Clé secrète pour Flask (assurez-vous de la changer pour plus de sécurité)
    SESSION_TYPE = 'filesystem'  # Type de session pour le stockage des cookies
    HOST = '127.0.0.1' # Adresse IP sur laquelle le serveur sera accessible
    PORT = 5000 # Port sur lequel le serveur sera accessible
