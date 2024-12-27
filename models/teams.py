from app import db  # Corrige le chemin d'import
from datetime import datetime
from sqlalchemy.orm import validates

class Team(db.Model):
    __tablename__ = 'teams'  # Ajout explicite du nom de la table

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Un nom d'équipe devrait être obligatoire
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pokemons = db.relationship('TeamPokemon', backref='team', lazy=True, cascade="all, delete-orphan")
    battles_as_team1 = db.relationship('Battle', foreign_keys='Battle.team1_id', backref='team1', lazy=True)
    battles_as_team2 = db.relationship('Battle', foreign_keys='Battle.team2_id', backref='team2', lazy=True)

    @validates('pokemons')
    def validate_pokemon_count(self, key, pokemon):
        if len(self.pokemons) >= 6:
            raise ValueError("Une équipe ne peut pas avoir plus de 6 Pokémon.")
        return pokemon
    
    def get_pokemon_count(self):
        return len(self.pokemons)
