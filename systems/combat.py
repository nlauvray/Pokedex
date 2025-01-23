from infrastructure.pokeapi import PokeApiClient

class CombatSystem:
    poke_api: PokeApiClient

    def __init__(self, poke_api: PokeApiClient):
        self.poke_api = poke_api
