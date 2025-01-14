from dataclasses import dataclass
from typing import Dict, List
from services.pokemon_services import PokemonApiService
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
    def get_move_by_name(cls, move_name: str):
        data = cls.moveApi.get(f"{move_name}")
        return cls.from_api_data(data)

@dataclass
class BattlePokemon:
    name: str
    stats: Dict[str, int]
    moves: List[Move]
    types: List[str]
    level: int = 50
    
    def __post_init__(self):
        self.current_hp = self.stats['hp']

    @classmethod
    def from_api_data(cls, data: Dict):
        print(data)
        moves = [Move.from_api_data(move['move']) for move in data['moves'][:4]] # Only the first 4 moves
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        types = [type_['type']['name'] for type_ in data['types']]
        return cls(
            name=data['name'],
            stats=stats,
            moves=moves,
            types=types
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
    def __init__(self, player_pokemon: BattlePokemon, opponent_pokemon: BattlePokemon):
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon

    def perform_move(self, attacker: BattlePokemon, defender: BattlePokemon, move: Move):
        if random.randint(1, 100) <= move.accuracy:
            damage = move.power  # Simplified damage calculation
            defender.current_hp -= damage
            return f"{attacker.name} used {move.name}! It dealt {damage} damage."
        else:
            return f"{attacker.name} used {move.name}! But it missed."
        
    def execute_turn(self, move_index: int) -> Dict:
        if not self.current_battle:
            raise ValueError("No active battle")

        player = self.current_battle['player']
        opponent = self.current_battle['opponent']
        
        # Player's turn
        player_move = player.moves[move_index]
        if player.current_pp[player_move.name] <= 0:
            self.current_battle['logs'].append(f"{player.name} cannot use {player_move.name}! No PP left!")
            return self.get_battle_state()

        damage = player.calculate_damage(player_move, opponent)
        opponent.current_hp = max(0, opponent.current_hp - damage)
        player.current_pp[player_move.name] -= 1

        # Add battle log
        effectiveness_text = self._get_effectiveness_text(damage, player_move, opponent)
        self.current_battle['logs'].append(
            f"{player.name} used {player_move.name}! {effectiveness_text}"
        )

        # Opponent's turn (if not fainted)
        if opponent.current_hp > 0:
            opponent_move = self._choose_opponent_move(opponent, player)
            damage = opponent.calculate_damage(opponent_move, player)
            player.current_hp = max(0, player.current_hp - damage)
            opponent.current_pp[opponent_move.name] -= 1

            effectiveness_text = self._get_effectiveness_text(damage, opponent_move, player)
            self.current_battle['logs'].append(
                f"{opponent.name} used {opponent_move.name}! {effectiveness_text}"
            )

        self.current_battle['turn'] += 1
        return self.get_battle_state()

    def _get_effectiveness_text(self, damage: int, move: Move, target: BattlePokemon) -> str:
        effectiveness = move.calculate_type_effectiveness(move.type, target.types)
        if effectiveness > 1.5:
            return "It's super effective!"
        elif effectiveness < 0.5:
            return "It's not very effective..."
        return ""

    def _choose_opponent_move(self, opponent: BattlePokemon, player: BattlePokemon) -> Move:
        # Simple AI: Choose a random move with PP remaining
        available_moves = [move for move in opponent.moves 
                         if opponent.current_pp[move.name] > 0]
        return random.choice(available_moves)

    def get_battle_state(self) -> Dict:
        if not self.current_battle:
            raise ValueError("No active battle")

        player = self.current_battle['player']
        opponent = self.current_battle['opponent']

        return {
            'player': {
                'name': player.name,
                'current_hp': player.current_hp,
                'max_hp': player.stats['hp'],
                'moves': [{
                    'name': move.name,
                    'pp': player.current_pp[move.name],
                    'max_pp': move.pp
                } for move in player.moves]
            },
            'opponent': {
                'name': opponent.name,
                'current_hp': opponent.current_hp,
                'max_hp': opponent.stats['hp']
            },
            'turn': self.current_battle['turn'],
            'logs': self.current_battle['logs'][-5:],
            'battle_over': player.current_hp <= 0 or opponent.current_hp <= 0
        }
        
def get_pokemon_data(pokemon_name: str):
    api_service = PokemonApiService()
    return api_service.get(f'pokemon/{pokemon_name}')