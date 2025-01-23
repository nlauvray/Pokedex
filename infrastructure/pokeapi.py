import requests

class PokeApiClient:
    def __init__(self, base_url: int):
        self.base_url = base_url

    def get_pokemons(self, limit: int = 20, offset: int = 0):
        url = f"{self.base_url}/pokemon?limit={limit}&offset={offset}"
        response = requests.get(url)
        return response.json()

    def get_pokemon(self, identifier: int or str):
        url = f"{self.base_url}/pokemon/{identifier}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Erreur lors de la récupération du Pokémon : {response.status_code}")
