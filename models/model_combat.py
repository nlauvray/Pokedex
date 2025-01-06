from . import db
from datetime import datetime

class Battle(db.Model):
    __tablename__ = 'battles'

    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)  # Gagnant facultatif
    battle_date = db.Column(db.DateTime, default=datetime.utcnow)
    turns = db.Column(db.Integer, default=0)
    battle_log = db.relationship(
        'BattleLog', backref='battle', lazy=True, cascade="all, delete-orphan"
    )

class BattleLog(db.Model):
    __tablename__ = 'battle_logs'

    id = db.Column(db.Integer, primary_key=True)
    battle_id = db.Column(db.Integer, db.ForeignKey('battles.id'), nullable=False)
    turn = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(200), nullable=False)
    attacker_id = db.Column(db.Integer, db.ForeignKey('team_pokemon.id'), nullable=True)
    defender_id = db.Column(db.Integer, db.ForeignKey('team_pokemon.id'), nullable=True)
    move_id = db.Column(db.Integer, db.ForeignKey('moves.id'), nullable=True)
    damage_dealt = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
