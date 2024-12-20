from infrastructure.pokeapi import PokeApiClient

class Pokemon:
    name: str

    def __init__(self, json):
        self.name = json["name"].capitalize()
        pass

    @staticmethod
    def get_from_api(api_client: PokeApiClient, identifier: int or str):
        json = api_client.get_pokemon(identifier)
        return Pokemon(json)

    @staticmethod
    def list_from_api(api_client: PokeApiClient, limit: int = 20, offset: int = 0):
        json = api_client.get_pokemons(limit, offset)
        return [get_from_api(api_client, p["name"]) for p in json["results"]]
