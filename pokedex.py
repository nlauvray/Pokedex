from flask import Flask, render_template
from infrastructure.pokeapi import PokeApiClient

from controllers import pokedex, pokemon

app = Flask(
    __name__,
    static_folder='./static',
    static_url_path='/static',
    template_folder='./templates'
)

pokeApi = PokeApiClient('https://pokeapi.co/api/v2')

app.register_blueprint(pokedex.get_routes())
app.register_blueprint(pokemon.get_routes(pokeApi))

if __name__ == '__main__':
    app.run()
