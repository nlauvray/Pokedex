from . import db
from datetime import datetime

class PokemonStatus(db.Model):
    __tablename__ = 'pokemon_status'

    id = db.Column(db.Integer, primary_key=True)
    fight_id = db.Column(db.Integer, db.ForeignKey('fights.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('team_pokemon.id'), nullable=False)
    hp = db.Column(db.Integer, nullable=False)

class Fight(db.Model):
    __tablename__ = 'fights'

    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team1_current_pokemon = db.Column(db.Integer, default=0)
    team2_current_pokemon = db.Column(db.Integer, default=0)
    winner_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)  # Gagnant facultatif
    battle_date = db.Column(db.DateTime, default=datetime.utcnow)

    statuses = db.relationship(
        'PokemonStatus', backref='fight', lazy=True, cascade="all, delete-orphan"
    )

    @property
    def team1_status(self):
        return [status for status in self.statuses if status.team_id == self.team1_id]

    @property
    def team2_status(self):
        return [status for status in self.statuses if status.team_id == self.team2_id]
