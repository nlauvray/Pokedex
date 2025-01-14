class Pokemon:
    def __init__(self, name, stats, types, abilities):
        self.name = name
        self.stats = stats
        self.types = types
        self.abilities = abilities

    @staticmethod
    def list_from_api(api_client):
        data = api_client.get('pokemon?limit=10')
        pokemons = []
        for item in data['results']:
            pokemon_data = api_client.get(f"pokemon/{item['name']}")
            pokemons.append(Pokemon(
                name=pokemon_data['name'],
                stats=pokemon_data['stats'],
                types=pokemon_data['types'],
                abilities=pokemon_data['abilities']
            ))
        return pokemons
