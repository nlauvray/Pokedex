from . import db  # Corrige le chemin d'import
from datetime import datetime
from sqlalchemy.orm import validates

class Team(db.Model):
    __tablename__ = 'teams'  # Ajout explicite du nom de la table

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Un nom d'équipe devrait être obligatoire
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pokemons = db.relationship('TeamPokemon', backref='team', lazy=True, cascade="all, delete-orphan")

    @validates('pokemons')
    def validate_pokemon_count(self, key, pokemon):
        if len(self.pokemons) >= 6:
            raise ValueError("Une équipe ne peut pas avoir plus de 6 Pokémon.")
        return pokemon
    
    def get_pokemon_count(self):
        return len(self.pokemons)

class TeamPokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)  # Correction ici
    pokemon_id = db.Column(db.Integer, nullable=False)
    position_in_team = db.Column(db.Integer)  # Position dans l'équipe (1-10)

    @validates('position_in_team')
    def validate_position(self, key, value):
        if value < 1 or value > 6:
            raise ValueError("La position dans l'équipe doit être comprise entre 1 et 6.")
        return value
