from flask import Flask
from controllers.routes import get_routes

app = Flask(
    __name__,
    static_folder='./static',
    static_url_path='/static',
    template_folder='./templates'
)

app.register_blueprint(get_routes())

if __name__ == '__main__':
    app.run()
