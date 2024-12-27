from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    teams = db.relationship('Team', backref='trainer', lazy=True)
    battles = db.relationship('Battle', backref='trainer', lazy=True)

    def set_pass(self, pwd):
        self.pwd = generate_password_hash(pwd)
    
    def check_pass(self, pwd):
        return check_password_hash(self.pwd, pwd)
    
    def get_teams(self):
        return len(self.teams)
