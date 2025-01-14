from dataclasses import dataclass
import random

@dataclass
class BattlePokemon:
    name: str
    stats: dict
    moves: list
    types: list
    sprites: dict
    level: int = 50

    def __post_init__(self):
        self.current_hp = self.stats['hp']

    def is_fainted(self):
        return self.current_hp <= 0

    def take_damage(self, amount):
        self.current_hp = max(0, self.current_hp - amount)
        return self.current_hp

    def calculate_damage(self, move, target):
        # Formule de dégâts Pokémon améliorée
        attack = self.stats['attack'] if move['category'] == 'physical' else self.stats['special-attack']
        defense = target.stats['defense'] if move['category'] == 'physical' else target.stats['special-defense']
        
        # Base damage calculation
        base_damage = ((2 * self.level / 5 + 2) * move['power'] * (attack / defense)) / 50 + 2
        
        # Random factor (85-100%)
        random_factor = random.randint(85, 100) / 100
        
        # Type effectiveness (simplifié pour l'exemple)
        type_bonus = 1.0  # À implémenter selon les types
        
        final_damage = int(base_damage * random_factor * type_bonus)
        return max(1, final_damage)  # Au moins 1 point de dégâts

    def get_random_move(self):
        return random.choice(self.moves)