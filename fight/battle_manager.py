from dataclasses import dataclass
from typing import Dict, List
from fight.battle import BattlePokemon
import random

@dataclass
class Move:
    name: str
    power: int
    accuracy: int
    pp: int
    type: str
    category: str

    def __init__(self, name: str, power: int, accuracy: int, pp: int, move_type: str, category: str):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.type = move_type
        self.category = category

    @classmethod
    def from_api_data(cls, data: Dict):
        return cls(
            name=data.get('name'),
            power=data.get('power', 0),
            accuracy=data.get('accuracy', 100),
            pp=data.get('pp', 0),
            move_type=data.get('type', {}).get('name', 'unknown'),
            category=data.get('damage_class', {}).get('name', 'unknown')
        )


    
@classmethod
def from_api_data(cls, data: Dict):
    moves = [Move.from_api_data(move['move']) for move in data['moves'][:4]] # Only the first 4 moves
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    types = [type_['type']['name'] for type_ in data['types']]
    sprites = data['sprites']
    return cls(
        name=data['name'],
        stats=stats,
        moves=moves,
        types=types,
        sprites=sprites
    )

def calculate_damage(self, move: Move, target: 'BattlePokemon') -> int:
    # Base damage calculation
    if move.category == 'physical':
        attack = self.stats['attack']
        defense = target.stats['defense']
    else:
        attack = self.stats['special-attack']
        defense = target.stats['special-defense']
    
    base_damage = ((2 * self.level / 5 + 2) * move.power * (attack / defense)) / 50 + 2
    
    # Type effectiveness calculation
    type_effectiveness = self.calculate_type_effectiveness(move.type, target.types)
    
    # Critical hit chance (1/16)
    critical = 1.5 if random.random() < 0.0625 else 1.0
    
    # Random factor (85-100%)
    random_factor = random.randint(85, 100) / 100
    
    final_damage = int(base_damage * type_effectiveness * critical * random_factor)
    return max(1, final_damage)

def calculate_type_effectiveness(self, move_type: str, target_types: List[str]) -> float:
    # Implement type effectiveness logic using type chart
    # This is a simplified version - you should implement the full type chart
    type_chart = {
        'water': {'fire': 2.0, 'ground': 2.0, 'rock': 2.0, 'water': 0.5, 'grass': 0.5},
        'fire': {'grass': 2.0, 'ice': 2.0, 'bug': 2.0, 'fire': 0.5, 'water': 0.5},
        'grass': {'water': 2.0, 'ground': 2.0, 'rock': 2.0, 'fire': 0.5, 'grass': 0.5},
        # Add more type relationships as needed
    }
    
    effectiveness = 1.0
    for target_type in target_types:
        if move_type in type_chart and target_type in type_chart[move_type]:
            effectiveness *= type_chart[move_type][target_type]
    
    return effectiveness

class BattleManager:
    def __init__(self, player_pokemons: List[BattlePokemon], opponent_pokemons: List[BattlePokemon]):
        self.player_pokemons = player_pokemons
        self.opponent_pokemons = opponent_pokemons
        self.player_pokemon = player_pokemons[0]
        self.opponent_pokemon = opponent_pokemons[0]

    def battle_turn(self, player_move: Move) -> str:
        # Player's turn
        damage = self.player_pokemon.calculate_damage(player_move, self.opponent_pokemon)
        self.opponent_pokemon.current_hp = max(0, self.opponent_pokemon.current_hp - damage)
        result = f"{self.player_pokemon.name} used {player_move.name}! It dealt {damage} damage."

        # Check if opponent fainted
        if self.opponent_pokemon.current_hp == 0:
            result += f" {self.opponent_pokemon.name} fainted!"
            return result

        # Opponent's turn
        opponent_move = random.choice(self.opponent_pokemon.moves)
        damage = self.opponent_pokemon.calculate_damage(opponent_move, self.player_pokemon)
        self.player_pokemon.current_hp = max(0, self.player_pokemon.current_hp - damage)
        result += f" {self.opponent_pokemon.name} used {opponent_move.name}! It dealt {damage} damage."

        # Check if player fainted
        if self.player_pokemon.current_hp == 0:
            result += f" {self.player_pokemon.name} fainted!"

        return result