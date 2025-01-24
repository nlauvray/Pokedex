from infrastructure.pokeapi import PokeApiClient
from models.teams import Team
from models.fight import Fight
from models.pokemon import Pokemon
from models.move import Move
import random

# Generate with AI from a chart, so there may be mistakes and/or hallucinations
TYPE_EFFECTIVENESS = {
    "normal": {
        "normal": 1, "fighting": 2, "flying": 1, "poison": 1, "ground": 1, "rock": 0.5, "bug": 1, "ghost": 0, "steel": 0.5, "fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 1, "ice": 1, "dragon": 1, "dark": 1, "fairy": 1
    },
    "fighting": {
        "normal": 2, "fighting": 1, "flying": 0.5, "poison": 0.5, "ground": 1, "rock": 2, "bug": 0.5, "ghost": 0, "steel": 2, "fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 0.5, "ice": 2, "dragon": 1, "dark": 2, "fairy": 0.5
    },
    "flying": {
        "normal": 1, "fighting": 2, "flying": 1, "poison": 1, "ground": 0, "rock": 0.5, "bug": 2, "ghost": 1, "steel": 0.5, "fire": 1, "water": 1, "grass": 2, "electric": 0.5, "psychic": 1, "ice": 1, "dragon": 1, "dark": 1, "fairy": 1
    },
    "poison": {
        "normal": 1, "fighting": 1, "flying": 1, "poison": 0.5, "ground": 0.5, "rock": 0.5, "bug": 1, "ghost": 0.5, "steel": 0, "fire": 1, "water": 1, "grass": 2, "electric": 1, "psychic": 1, "ice": 1, "dragon": 1, "dark": 1, "fairy": 2
    },
    "ground": {
        "normal": 1, "fighting": 1, "flying": 1, "poison": 2, "ground": 1, "rock": 2, "bug": 0.5, "ghost": 1, "steel": 2, "fire": 2, "water": 1, "grass": 0.5, "electric": 2, "psychic": 1, "ice": 1, "dragon": 1, "dark": 1, "fairy": 1
    },
    "rock": {
        "normal": 1, "fighting": 0.5, "flying": 2, "poison": 1, "ground": 0.5, "rock": 1, "bug": 2, "ghost": 1, "steel": 0.5, "fire": 2, "water": 1, "grass": 1, "electric": 1, "psychic": 1, "ice": 2, "dragon": 1, "dark": 1, "fairy": 1
    },
    "bug": {
        "normal": 1, "fighting": 0.5, "flying": 0.5, "poison": 0.5, "ground": 1, "rock": 1, "bug": 1, "ghost": 0.5, "steel": 0.5, "fire": 0.5, "water": 1, "grass": 2, "electric": 1, "psychic": 2, "ice": 1, "dragon": 1, "dark": 2, "fairy": 0.5
    },
    "ghost": {
        "normal": 0, "fighting": 1, "flying": 1, "poison": 1, "ground": 1, "rock": 1, "bug": 1, "ghost": 2, "steel": 1, "fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 2, "ice": 1, "dragon": 1, "dark": 0.5, "fairy": 1
    },
    "steel": {
        "normal": 1, "fighting": 1, "flying": 1, "poison": 1, "ground": 1, "rock": 2, "bug": 1, "ghost": 1, "steel": 0.5, "fire": 0.5, "water": 0.5, "grass": 1, "electric": 0.5, "psychic": 1, "ice": 2, "dragon": 1, "dark": 1, "fairy": 2
    },
    "fire": {
        "normal": 1, "fighting": 1, "flying": 1, "poison": 1, "ground": 1, "rock": 0.5, "bug": 2, "ghost": 1, "steel": 2, "fire": 0.5, "water": 0.5, "grass": 2, "electric": 1, "psychic": 1, "ice": 2, "dragon": 0.5, "dark": 1, "fairy": 1
    },
    "water": {
        "normal": 1, "fighting": 1, "flying": 1, "poison": 1, "ground": 2, "rock": 2, "bug": 1, "ghost": 1, "steel": 1, "fire": 2, "water": 0.5, "grass": 0.5, "electric": 1, "psychic": 1, "ice": 1, "dragon": 0.5, "dark": 1, "fairy": 1
    },
    "grass": {
        "normal": 1, "fighting": 1, "flying": 0.5, "poison": 0.5, "ground": 2, "rock": 2, "bug": 0.5, "ghost": 1, "steel": 0.5, "fire": 0.5, "water": 2, "grass": 0.5, "electric": 1, "psychic": 1, "ice": 1, "dragon": 0.5, "dark": 1, "fairy": 1
    },
    "electric": {
        "normal": 1, "fighting": 1, "flying": 2, "poison": 1, "ground": 0, "rock": 1, "bug": 1, "ghost": 1, "steel": 1, "fire": 1, "water": 2, "grass": 0.5, "electric": 0.5, "psychic": 1, "ice": 1, "dragon": 0.5, "dark": 1, "fairy": 1
    },
    "psychic": {
        "normal": 1, "fighting": 2, "flying": 1, "poison": 2, "ground": 1, "rock": 1, "bug": 1, "ghost": 1, "steel": 0.5, "fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 0.5, "ice": 1, "dragon": 1, "dark": 0, "fairy": 1
    },
    "ice": {
        "normal": 1, "fighting": 1, "flying": 2, "poison": 1, "ground": 2, "rock": 1, "bug": 1, "ghost": 1, "steel": 0.5, "fire": 0.5, "water": 0.5, "grass": 2, "electric": 1, "psychic": 1, "ice": 0.5, "dragon": 2, "dark": 1, "fairy": 1
    },
    "dragon": {
        "normal": 1, "fighting": 1, "flying": 1, "poison": 1, "ground": 1, "rock": 1, "bug": 1, "ghost": 1, "steel": 0.5, "fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 1, "ice": 1, "dragon": 2, "dark": 1, "fairy": 0
    },
    "dark": {
        "normal": 1, "fighting": 0.5, "flying": 1, "poison": 1, "ground": 1, "rock": 1, "bug": 1, "ghost": 2, "steel": 1, "fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 2, "ice": 1, "dragon": 1, "dark": 0.5, "fairy": 0.5
    },
    "fairy": {
        "normal": 1, "fighting": 2, "flying": 1, "poison": 0.5, "ground": 1, "rock": 1, "bug": 1, "ghost": 1, "steel": 0.5, "fire": 0.5, "water": 1, "grass": 1, "electric": 1, "psychic": 1, "ice": 1, "dragon": 2, "dark": 2, "fairy": 1
    }
}

class FightSystem:
    poke_api: PokeApiClient

    def __init__(self, poke_api: PokeApiClient):
        self.poke_api = poke_api

    def start_fight(self, player_team: Team, opponent_team: Team):
        assert player_team.trainer_id == opponent_team.trainer_id, "A trainer may only fight against one of its own teams"
        fight = Fight(trainer_id=player_team.trainer_id, team1_id=player_team.id, team2_id=opponent_team.id, team1_current_pokemon=0, team2_current_pokemon=0, turns=0)
        for pokemon in player_team.pokemons:
            fight.statuses.append(PokemonStatus(fight_id=fight.id, team_id=player_team.id, pokemon_id=pokemon.id, hp=Pokemon.get_from_api(self.poke_api, pokemon).stats['hp'].base_stat))
        for pokemon in opponent_team.pokemons:
            fight.team2_status.append(PokemonStatus(fight_id=fight.id, team_id=opponent_team.id, pokemon_id=pokemon.id, hp=Pokemon.get_from_api(self.poke_api, pokemon).stats['hp'].base_stat))

        db.session.add(fight)
        db.session.commit()

        return fight

    def turn(self, fight: Fight, current_player: int, move_id: int):
        current_team = fight.team1 if current_player == 1 else fight.team2
        opponent_team = fight.team2 if current_player == 1 else fight.team1

        current_pokemon = Pokemon.get_from_api(self.poke_api, current_team.pokemons[current_team.team1_current_pokemon])
        opponent_pokemon = Pokemon.get_from_api(self.poke_api, opponent_team.pokemons[current_team.team2_current_pokemon])
        move = Move.get_from_api(self.poke_api, move_id)

        current_team_status = fight.team2_status if current_player == 2 else fight.team1_status
        current_pokemon_status = opponent_team_status[opponent_team.team2_current_pokemon if current_player == 2 else opponent_team.team1_current_pokemon]
        if current_pokemon_status.hp <= 0:
            return False

        # Damage calculation taken from https://bulbapedia.bulbagarden.net/wiki/Damage
        # damage = ((((2 * level * critical)/5 + 2) * power * attack / defense) / 50 + 2) * stab * type1 * type2 * random

        level = 1 # TODO: Pokemons do not have levels here.

        critical_thresold = max(current_pokemon.stats['speed'].base_stat / 2, 255)

        if random.randint(0, 255) < critical_thresold:
            critical = 2
        else:
            critical = 1

        power = move.power
        if move.damage_class == "physical":
            attack = current_pokemon.stats['attack'].base_stat
            defense = opponent_pokemon.stats['defense'].base_stat
        else:
            attack = current_pokemon.stats['special-attack'].base_stat
            defense = opponent_pokemon.stats['special-defense'].base_stat

        if attack > 255 or defense > 255:
            attack = attack // 4
            defense = defense // 4

        if move.type in current_pokemon.types:
            stab = 1.5
        else:
            stab = 1

        type1 = type_effectiveness(move.type, opponent_pokemon.types, 1)
        type2 = type_effectiveness(move.type, opponent_pokemon.types, 2)

        damage = ((((2 * level * critical)/5 + 2) * power * attack / defense) / 50 + 2) * stab * type1 * type2
        opponent_team_status = fight.team1_status if current_player == 2 else fight.team2_status
        opponent_pokemon_status = opponent_team_status[opponent_team.team2_current_pokemon if current_player == 1 else opponent_team.team1_current_pokemon]
        opponent_pokemon_status.hp -= damage

        db.session.commit()

        return opponent_pokemon_status.hp

    def change_pokemon(self, fight: Fight, current_player: int, slot: int):
        current_team = fight.team1 if current_player == 1 else fight.team2
        current_team_status = fight.team1_status if current_player == 1 else fight.team2_status
        next_pokemon = current_team.pokemons[slot]
        next_pokemon_status = current_team_status[slot]

        if next_pokemon_status.hp > 0:
            current_team.team1_current_pokemon = slot
            done = True
        else:
            done = False

        db.session.commit()

        return done

    def type_effectiveness(self, move_type, opponent_types, position):
        count = 0
        effectiveness = 1
        for opponent_type in opponent_types:
            if TYPE_EFFECTIVENESS[move_type][opponent_type] == position:
                count += 1
                effectiveness = TYPE_EFFECTIVENESS[move_type][opponent_type]
                if count == position:
                    break

        return effectiveness
