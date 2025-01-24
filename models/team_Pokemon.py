from . import db 
from . teams import Team
from sqlalchemy.orm import validates

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
