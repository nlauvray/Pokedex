import requests
from typing import Union

class PokeApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}")
        if response.status_code != 200:
            raise ValueError(f"Erreur lors de la récupération des données: {response.status_code}")
        return response.json()

    def get_pokemon(self, name):
        response = requests.get(f"{self.base_url}/pokemon/{name}")
        if response.status_code == 404:
            raise ValueError(f"Pokémon non trouvé: {name}")
        elif response.status_code != 200:
            raise ValueError(f"Erreur lors de la récupération du Pokémon: {response.status_code}")
        return response.json()

    def get_move(self, move_name: str):
        url = f"{self.base_url}/move/{move_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        raise ValueError(f"Erreur lors de la récupération du mouvement: {response.status_code}")
