class MoveService:
    def __init__(self, api_client):
        self.api_client = api_client
        self._move_cache = {}  # Cache pour les mouvements

    def get_move(self, move_name):
        if move_name not in self._move_cache:
            move_data = self.api_client.get_move(move_name)
            self._move_cache[move_name] = {
                'name': move_data['name'],
                'power': move_data.get('power', 40),  # Valeur par défaut si power est None
                'accuracy': move_data.get('accuracy', 100),
                'pp': move_data['pp'],
                'type': move_data['type']['name'],
                'category': move_data['damage_class']['name']
            }
        return self._move_cache[move_name]