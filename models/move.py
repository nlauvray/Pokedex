from infrastructure.pokeapi import PokeApiClient

class MoveContestCombo:
    use_before: list[str]
    use_after: list[str]

    def __init__(self, json):
        self.use_before = [u["name"] for u in json["use_before"]]
        self.use_after = [u["name"] for u in json["use_after"]]

class MoveContestCombos:
    normal: MoveContestCombo
    super: MoveContestCombo

    def __init__(self, json):
        self.normal = MoveContestCombo(json["normal"])
        self.super = MoveContestCombo(json["super"])

class MoveEffect:
    effect: str
    language: str
    short_effect: str

    def __init__(self, json):
        self.effect = json["effect"]
        self.language = json["language"]["name"]
        self.short_effect = json["short_effect"]

class MoveEffectChange:
    effect_entries: list[MoveEffect]
    version_group: str

    def __init__(self, json):
        self.effect_entries = [MoveEffect(e) for e in json["effect_entries"]]
        self.version_group = json["version_group"]["name"]

class MoveMeta:
    ailment: str
    category: str
    min_hits: int
    max_hits: int
    min_turns: int
    max_turns: int
    drain: int
    healing: int
    crit_rate: int
    ailment_chance: int
    flinch_chance: int
    stat_chance: int

    def __init__(self, json):
        self.ailment = json["ailment"]["name"]
        self.category = json["category"]["name"]
        self.min_hits = json["min_hits"]
        self.max_hits = json["max_hits"]
        self.min_turns = json["min_turns"]
        self.max_turns = json["max_turns"]
        self.drain = json["drain"]
        self.healing = json["healing"]
        self.crit_rate = json["crit_rate"]
        self.ailment_chance = json["ailment_chance"]
        self.flinch_chance = json["flinch_chance"]
        self.stat_chance = json["stat_chance"]

class MovePastStatValues:
    accuracy: int
    effect_chance: int
    power: int
    pp: int
    effect_entries: list[MoveEffect]
    type: str
    version_group: str

    def __init__(self, json):
        self.accuracy = json["accuracy"]
        self.effect_chance = json["effect_chance"]
        self.power = json["power"]
        self.pp = json["pp"]
        self.effect_entries = [MoveEffect(e) for e in json["effect_entries"]]
        self.type = json["type"]["name"]
        self.version_group = json["version_group"]["name"]

class MoveFlavorText:
    flavor_text: str
    language: str
    version_group: str

    def __init__(self, json):
        self.flavor_text = json["flavor_text"]
        self.language = json["language"]["name"]
        self.version_group = json["version_group"]["name"]

class Move:
    id: int
    name: str
    accuracy: int
    effect_chance: int
    pp: int
    priority: int
    power: int
    contest_combos: MoveContestCombos
    contest_type: str
    contest_effect: str
    damage_class: str
    effect_entries: list[MoveEffect]
    effect_changes: list[MoveEffectChange]
    generation: str
    meta: MoveMeta
    names: list[str]
    past_values: MovePastStatValues
    stat_changes: dict[str, int]
    super_contest_effect: str
    target: str
    type: str
    learned_by_pokemon: list[str]
    flavor_text_entries: list[MoveFlavorText]

    def __init__(self, json):
        self.id = json["id"]
        self.name = json["name"].capitalize()
        self.accuracy = json["accuracy"]
        self.effect_chance = json["effect_chance"]
        self.pp = json["pp"]
        self.priority = json["priority"]
        self.power = json["power"]
        self.contest_combos = MoveContestCombos(json["contest_combos"])
        self.contest_type = json["contest_type"]["name"]
        self.contest_effect = json["contest_effect"]
        self.damage_class = json["damage_class"]["name"]
        self.effect_entries = [MoveEffect(e) for e in json["effect_entries"]]
        self.effect_changes = [MoveEffectChange(e) for e in json["effect_changes"]]
        self.generation = json["generation"]["name"]
        self.meta = MoveMeta(json["meta"])
        self.names = [n["name"] for n in json["names"]]
        self.past_values = MovePastStatValues(json["past_values"])
        self.stat_changes = {s["stat"]["name"]: s["change"] for s in json["stat_changes"]}
        self.super_contest_effect = json["super_contest_effect"]
        self.target = json["target"]["name"]
        self.type = json["type"]["name"]
        self.learned_by_pokemon = [p["name"] for p in json["learned_by_pokemon"]]
        self.flavor_text_entries = [MoveFlavorText(f) for f in json["flavor_text_entries"]]

    @staticmethod
    def get_from_api(api_client: PokeApiClient, identifier: int or str):
        json = api_client.get_move(identifier)
        return Pokemon(json)

    @staticmethod
    def list_from_api(api_client: PokeApiClient, limit: int = 20, offset: int = 0):
        json = api_client.get_moves(limit, offset)
        return [get_from_api(api_client, p["name"]) for p in json["results"]]
