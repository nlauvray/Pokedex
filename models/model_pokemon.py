from . import db

class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    pokedex_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    types = db.Column(db.String(50))  # Format: "type1,type2"
    base_stats = db.Column(db.JSON)  # {"hp": 100, "attack": 90, etc.}
    sprite_url = db.Column(db.String(200))
    
    # Relation avec Move via la table associative PokemonMoves
    moves = db.relationship(
        'Move', secondary='pokemon_moves', back_populates='pokemons', lazy='dynamic'
    )

class Move(db.Model):
    __tablename__ = 'moves'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # Exemple: "fire", "water"
    power = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)

    # Relation avec Pokemon via la table associative PokemonMoves
    pokemons = db.relationship(
        'Pokemon', secondary='pokemon_moves', back_populates='moves', lazy='dynamic'
    )

class PokemonMoves(db.Model):
    __tablename__ = 'pokemon_moves'

    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)  # Clé étrangère vers Pokemon
    move_id = db.Column(db.Integer, db.ForeignKey('moves.id'), nullable=False)  # Clé étrangère vers Move

    # Pas de relations supplémentaires ici, car elles ne sont pas nécessaires
