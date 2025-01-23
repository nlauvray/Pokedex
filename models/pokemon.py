from infrastructure.pokeapi import PokeApiClient

class PokemonAbility:
    is_hidden: bool
    slot: int
    ability: str

    def __init__(self, json):
        self.is_hidden = json["is_hidden"]
        self.slot = json["slot"]
        self.ability = json["ability"]["name"]

class PokemonGameIndex:
    game_index: int
    version: str

    def __init__(self, json):
        self.game_inde = json["game_index"]
        self.version = json["version"]["name"]

class PokemonHeldItemVersionDetails:
    rarity: int
    version: str

    def __init__(self, json):
        self.rarity = json["rarity"]
        self.version = json["version"]["name"]

class PokemonHeldItem:
    item: str
    version_details: list[PokemonHeldItemVersionDetails]

    def __init__(self, json):
        self.item = json["item"]["name"]
        self.version_details = [PokemonHeldItemVersionDetails(v) for v in json["version_details"]]

class PokemonMoveVersionGroupDetails:
    level_learned_at: int
    move_learn_method: str
    version_group: str

    def __init__(self, json):
        self.level_learned_at = json["level_learned_at"]
        self.move_learn_method = json["move_learn_method"]["name"]
        self.version_group = json["version_group"]["name"]

class PokemonMove:
    move: str
    version_group_details: list[PokemonMoveVersionGroupDetails]

    def __init__(self, json):
        self.move = json["move"]["name"]
        self.version_group_details = [PokemonMoveVersionGroupDetails(v) for v in json["version_group_details"]]

class PokemonStat:
    base_stat: int
    effort: int
    name: str

    def __init__(self, json):
        self.base_stat = json["base_stat"]
        self.effort = json["effort"]
        self.name = json["stat"]["name"]

class PokemonSprites:
    back_default: str
    back_female: str
    back_shiny: str
    back_shiny_female: str
    front_default: str
    front_female: str
    front_shiny: str
    front_shiny_female: str

    def __init__(self, json):
        self.back_default = json["back_default"]
        self.back_female = json["back_female"]
        self.back_shiny = json["back_shiny"]
        self.back_shiny_female = json["back_shiny_female"]
        self.front_default = json["front_default"]
        self.front_female = json["front_female"]
        self.front_shiny = json["front_shiny"]
        self.front_shiny_female = json["front_shiny_female"]

class PokemonType:
    slot: int
    name: str

    def __init__(self, json):
        self.slot = json["slot"]
        self.name = json["type"]["name"]

class PokemonPastType:
    generation: str
    types: list[PokemonType]

    def __init__(self, json):
        self.generation = json["generation"]["name"]
        self.types = [PokemonType(t) for t in json["types"]]

class Pokemon:
    id: int
    name: str
    base_experience: int
    height: int
    is_default: bool
    order: int
    weight: int
    abilities: list[PokemonAbility]
    forms: list[str]
    game_indices: list[PokemonGameIndex]
    held_items: list[str]
    location_area_encounters: str
    moves: list[PokemonMove]
    species: str
    sprites: PokemonSprites
    cries: str
    stats: list[PokemonStat]
    types: list[PokemonType]
    past_types: list[PokemonPastType]

    def __init__(self, json):
        self.id = json["id"]
        self.name = json["name"].capitalize()
        self.base_experience = json["base_experience"]
        self.height = json["height"]
        self.is_default = json["is_default"]
        self.order = json["order"]
        self.weight = json["weight"]
        self.abilities = [PokemonAbility(a) for a in json["abilities"]]
        self.forms = [f["name"] for f in json["forms"]]
        self.game_indices = [PokemonGameIndex(g) for g in json["game_indices"]]
        self.held_items = [h["item"]["name"] for h in json["held_items"]]
        self.location_area_encounters = json["location_area_encounters"]
        self.moves = [PokemonMove(m) for m in json["moves"]]
        self.species = json["species"]["name"]
        self.sprites = PokemonSprites(json["sprites"])
        self.cries = json["species"]["name"]
        self.stats = [PokemonStat(s) for s in json["stats"]]
        self.types = [PokemonType(t) for t in json["types"]]
        self.past_types = [PokemonPastType(p) for p in json["past_types"]]

    @staticmethod
    def get_from_api(api_client: PokeApiClient, identifier: int or str):
        json = api_client.get_pokemon(identifier)
        return Pokemon(json)

    @staticmethod
    def list_from_api(api_client: PokeApiClient, limit: int = 20, offset: int = 0):
        json = api_client.get_pokemons(limit, offset)
        return [Pokemon.get_from_api(api_client, p["name"]) for p in json["results"]]

    @staticmethod
    def search_from_api(api_client: PokeApiClient, query: str, limit: int = 20, offset: int = 0):
        if query == "":
            return Pokemon.count(api_client), Pokemon.list_from_api(api_client, limit, offset)
        json = api_client.get_pokemons(-1, 0)

        results = []
        for p in json["results"]:
            if query.lower() in p["name"].lower():
                results.append(Pokemon.get_from_api(api_client, p["name"]))

        offset = min(offset, len(results)-1)
        end = min(offset + limit, len(results))
        return len(results), results[offset:end]

    @staticmethod
    def count(api_client: PokeApiClient):
        json = api_client.get_pokemons()
        return json["count"]
