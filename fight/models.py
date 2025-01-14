class BattlePokemon:
    def __init__(self, name, level, max_hp, current_hp, moves):
        self.name = name
        self.level = level
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.moves = moves

    def take_damage(self, amount):
        self.current_hp = max(0, self.current_hp - amount)
        return self.current_hp

    def is_fainted(self):
        return self.current_hp <= 0