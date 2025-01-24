# Pokedex
Une application web pour rechercher des pokémons, créer des équipes et les faire combattre.

## Pré-requis

- Python 3.13+ (une version ultérieure peut fonctionner, mais ça n'a pas été testé)

## Installation

Créez et activez un environnement virtuel:
```bash
python -m venv venv
# Windows - CMD
venv\Scripts\activate

# Windows - PowerShell
venv\Scripts\activate.ps1

# Unix
source venv/bin/activate
```

Installez les dépendences:
```bash
pip install -r requirements.txt
```

## Configuration

La configuration de l'application se fait dans le fichier `config.py`.
Nous vous recommandons de modifier au minimum la variable `SECRET_KEY`, qui permet de sécuriser les sessions de l'application.

## Utilisation

Lancer simplement le serveur avec la commande suivante:
```bash
python pokedex.py
```

Au lancement, et si ces fichiers n'existent pas, l'application va créer les certificats `rsa_public.pem` et `rsa_private.pem` pour chiffrer les mots de passes utilisateurs, et la base de donnée SQLite si l'URI configurée correspond à une base de donnée SQLite.

L'application sera lancée sur l'addresse configurée dans `config.py` (par exemple `http://localhost:5000`).

## Documentation utilisateur

La page principale de l'application présente un pokédex, sur lequel les utilisateurs peuvent rechercher des pokémons et voir leur détails.

Pour créer des équipes et faire des combats, les utilisateurs doivent être authentifié.
Vous pouvez voir et gérer vos équipes depuis votre profil.
Pour le moment, l'interface des combats n'est pas disponible. Cependant, une API est disponible.

## Documentation technique

Cette application est construite autour de Flask et SQLAlchemy. Elle utilise l'API [PokeAPI](https://pokeapi.co/) pour obtenir les données des pokémons.

L'application est structurée de la façon suivante :
- `config.py` : Configuration de l'application
- `pokedex.py` : Point d'entrée de l'application, configure et lance le serveur
- `controllers/` : Contrôleurs de l'application. Chaque contrôleurs définit une fonction `get_routes` qui prend en paramètre les systèmes nécessaire à l'exécution des contrôleurs, et retourne un blueprint Flask, qui sera ajouté à l'application
- `models/` : Modèles de données pour l'application. Il y a deux types de modèles : les modèles API, et les modèles SQLAlchemy
- `systems/`: Systèmes de l'application. Ils contiennent les fonctions métiers de l'application
- `infrastructure/` : Interfaces externes de l'application. Pour le moment, seul une interface pour l'API PokeAPI est implémenté
- `templates/` : Templates HTML de l'application.
- `static/` : Fichiers statiques (CSS, JS, images, etc.) de l'application
