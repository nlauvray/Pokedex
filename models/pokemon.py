from infrastructure.pokeapi import PokeApiClient

class Pokemon:
    name: str
    image_url: str
    types: list
    stats: list

    def __init__(self, json):
        self.name = json["name"]
        self.image_url = json["sprites"]["front_default"]
        self.types = [t["type"]["name"] for t in json["types"]]
        self.stats = {stat["stat"]["name"]: stat["base_stat"] for stat in json["stats"]}
        pass

    @staticmethod
    def get_from_api(api_client: PokeApiClient, identifier: int or str):
        json = api_client.get_pokemon(identifier)
        return Pokemon(json)

    @staticmethod
    def list_from_api(api_client: PokeApiClient, limit: int = 20, offset: int = 0):
        json = api_client.get_pokemons(limit, offset)
        return [Pokemon.get_from_api(api_client, p["name"]) for p in json["results"]]
