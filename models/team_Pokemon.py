from . import db 
from . teams import Team
from sqlalchemy.orm import validates

class TeamPokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)  # Correction ici
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    nickname = db.Column(db.String(50))
    level = db.Column(db.Integer, default=5)
    current_hp = db.Column(db.Integer)
    moves = db.Column(db.JSON)  # Liste des IDs des moves: [1, 2, 3, 4]
    stats = db.Column(db.JSON)  # Stats calculées selon le niveau
    position_in_team = db.Column(db.Integer)  # Position dans l'équipe (1-10)

    @validates('moves')
    def validates_moves(self, key, value):
        if len(value) > 4:
            raise ValueError("Un pokémon ne peut avoir que 4 mouvements")
        return value
    
    @validates('position_in_team')
    def validate_position(self, key, value):
        if value < 1 or value > 6:
            raise ValueError("La position dans l'équipe doit être comprise entre 1 et 6.")
        return value
