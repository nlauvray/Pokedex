from infrastructure.pokeapi import PokeApiClient
from typing import Dict, List, Optional

class PokemonApiService:
    """Service centralisé pour gérer tous les appels API Pokémon"""
    
    def __init__(self):
        self.base_url = 'https://pokeapi.co/api/v2'
        self.api_clients = {
            'pokemon': PokeApiClient(self.base_url),
            'ability': PokeApiClient(f'{self.base_url}/ability'),
            'type': PokeApiClient(f'{self.base_url}/type'),
            'stat': PokeApiClient(f'{self.base_url}/stat'),
            'move': PokeApiClient(f'{self.base_url}/move'),
            'move_damage_class': PokeApiClient(f'{self.base_url}/move-damage-class'),
            'move_category': PokeApiClient(f'{self.base_url}/move-category'),
            'encounter_condition': PokeApiClient(f'{self.base_url}/encounter-condition'),
            'nature': PokeApiClient(f'{self.base_url}/nature'),
            'item': PokeApiClient(f'{self.base_url}/item'),
            'berry': PokeApiClient(f'{self.base_url}/berry')
        }
        self._cache = {}

    def get_pokemon_complete_data(self, pokemon_id: int) -> Dict:
        """Récupère toutes les données d'un Pokémon avec ses capacités, types, etc."""
        cache_key = f'pokemon_{pokemon_id}'
        if cache_key in self._cache:
            return self._cache[cache_key]

        pokemon_data = self.api_clients['pokemon'].get_pokemon(pokemon_id)
        
        # Enrichir les données avec les détails supplémentaires
        complete_data = {
            'base_info': pokemon_data,
            'abilities': self._get_abilities(pokemon_data['abilities']),
            'types': self._get_types(pokemon_data['types']),
            'stats': self._get_stats(pokemon_data['stats']),
            'moves': self._get_moves(pokemon_data['moves'][:4]) # Seulement les 4 premières attaques
        }

        self._cache[cache_key] = complete_data
        return complete_data

    def _get_abilities(self, abilities_data: List) -> List[Dict]:
        """Récupère les détails des capacités"""
        return [
            self.api_clients['ability'].get_pokemon(ability['ability']['name'])
            for ability in abilities_data
        ]

    def _get_types(self, types_data: List) -> List[Dict]:
        """Récupère les détails des types"""
        return [
            self.api_clients['type'].get_pokemon(type_data['type']['name'])
            for type_data in types_data
        ]

    def _get_stats(self, stats_data: List) -> Dict:
        """Formate les statistiques"""
        return {
            stat_data['stat']['name']: {
                'base_value': stat_data['base_stat'],
                'details': self.api_clients['stat'].get_pokemon(stat_data['stat']['name'])
            }
            for stat_data in stats_data
        }

    def _get_moves(self, moves_data: List) -> List[Dict]:
        """Récupère les détails des attaques"""
        moves = []
        for move_data in moves_data:
            move_details = self.api_clients['move'].get_pokemon(move_data['move']['name'])
            
            # Enrichir avec la catégorie de dégâts
            damage_class = self.api_clients['move_damage_class'].get_pokemon(
                move_details['damage_class']['name']
            )
            
            moves.append({
                'name': move_details['name'],
                'power': move_details.get('power', 0),
                'accuracy': move_details.get('accuracy', 100),
                'pp': move_details['pp'],
                'type': move_details['type']['name'],
                'damage_class': damage_class,
                'category': move_details.get('category', {})
            })
        
        return moves

    def get_items(self) -> List[Dict]:
        """Récupère la liste des objets disponibles"""
        return self.api_clients['item'].get_pokemons(limit=20)

    def get_berries(self) -> List[Dict]:
        """Récupère la liste des baies disponibles"""
        return self.api_clients['berry'].get_pokemons(limit=20)

    def get_natures(self) -> List[Dict]:
        """Récupère la liste des natures"""
        return self.api_clients['nature'].get_pokemons(limit=25)