import requests

class PokeApiClient:
    def __init__(self, base_url: int):
        self.base_url = base_url

    def get_pokemons(self, limit: int = 20, offset: int = 0):
        url = f"{self.base_url}/pokemon?limit={limit}&offset={offset}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Une erreur est survenu pendant la récupération des pokemons. Veuillez réessayer plus tard.")

        return response.json()

    def get_pokemon(self, identifier: int or str): # type: ignore
        url = f"{self.base_url}/pokemon/{identifier}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Une erreur est survenu pendant la récupération du pokemon. Veuillez reéssayer plus tard.")

        return response.json()

    def get_moves(self, limit: int = 20, offset: int = 0):
        url = f"{self.base_url}/move"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Une erreur est survenu pendant la récupération des moves. Veuillez reéssayer plus tard.")

        return response.json()

    def get_move(self, identifier: int or str): # type: ignore
        url = f"{self.base_url}/move/{identifier}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Une erreur est survenu pendant la récupération du move. Veuillez reéssayer plus tard.")

        return response.json()
