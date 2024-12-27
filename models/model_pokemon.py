from . import db

class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    pokedex_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    types = db.Column(db.String(50))  # Format: "type1,type2"
    base_stats = db.Column(db.JSON)  # {"hp": 100, "attack": 90, etc.}
    sprite_url = db.Column(db.String(200))
    moves = db.relationship('Move', secondary='pokemon_moves', lazy='dynamic')  # Relation avec la table associative

class Move(db.Model):
    __tablename__ = 'moves'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    power = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    pp = db.Column(db.Integer)

class PokemonMoves(db.Model):
    __tablename__ = 'pokemon_moves'
    
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))  # Clé étrangère vers 'pokemon'
    move_id = db.Column(db.Integer, db.ForeignKey('moves.id'))  # Clé étrangère vers 'moves'
    
    # Relations (ce n'est pas nécessaire ici, mais utile pour les jointures)
    pokemon = db.relationship('Pokemon', backref=db.backref('pokemon_moves', lazy=True))
    move = db.relationship('Move', backref=db.backref('pokemon_moves', lazy=True))
