import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify
from models import db
from models.users import User
from models.pokemon import Pokemon
from models.teams import Team, TeamPokemon
from systems.auth import AuthSystem
from infrastructure.pokeapi import PokeApiClient

def get_routes():
    bp = Blueprint('teams', __name__, url_prefix='/teams')

    # Route pour créer une équipe
    @bp.route('/create', methods=['GET', 'POST'])
    @AuthSystem.login_required
    def create_team():
        user = User.query.get(session['user_id'])
        
        poke_api_client = PokeApiClient(base_url='https://pokeapi.co/api/v2')
        pokemons = Pokemon.list_from_api(poke_api_client)
        
        if request.method == 'POST':
            team_name = request.form['team_name']
            selected_pokemons = request.form.get('pokemons').split(',')
            
            if len(selected_pokemons) > 5:
                flash('Vous ne pouvez ajouter que jusqu\'à 5 Pokémon dans une équipe.', 'error')
                return redirect(url_for('teams.create_team'))
            
            new_team = Team(name=team_name, trainer_id=user.id)
            db.session.add(new_team)
            db.session.commit()
            
            for pokemon_id in selected_pokemons:
                team_pokemon = TeamPokemon(team_id=new_team.id, pokemon_id=pokemon_id)
                db.session.add(team_pokemon)
                
            db.session.commit()
            
            return redirect(url_for('teams.get_team', team_id=new_team.id))
        
        return render_template('create_team.html', user=user, pokemons=pokemons)

    # Route pour afficher une équipe
    @bp.route('/<int:team_id>', methods=['GET'])
    @AuthSystem.login_required
    def get_team(team_id):
        team = Team.query.get_or_404(team_id)
        poke_api_client = PokeApiClient(base_url='https://pokeapi.co/api/v2')
        all_pokemons = Pokemon.list_from_api(poke_api_client)
        team_pokemons = TeamPokemon.query.filter_by(team_id=team_id).all()
        pokemons = [Pokemon.get_from_api(poke_api_client, pokemon.pokemon_id) for pokemon in team_pokemons]
        return render_template('team.html', team=team, all_pokemons=all_pokemons, team_pokemons=pokemons)

    @bp.route('/<int:team_id>/update', methods=['POST'])
    @AuthSystem.login_required
    def update_team(team_id):
        team = Team.query.get_or_404(team_id)
        pokemons = request.json.get('selectedPokemons', [])

        current_pokemons = TeamPokemon.query.filter_by(team_id=team.id).all()
        for pokemon in current_pokemons:
            db.session.delete(pokemon)

        for pokemon_id in pokemons:
            team_pokemon = TeamPokemon(team_id=team.id, pokemon_id=pokemon_id)
            db.session.add(team_pokemon)

        db.session.commit()
        return jsonify({'success': True})

    # Route pour supprimer une équipe
    @bp.route('/<int:team_id>', methods=['DELETE'])
    @AuthSystem.login_required
    def delete_team(team_id):
        team = Team.query.get_or_404(team_id)
        
        db.session.delete(team)
        db.session.commit()
        flash('Équipe supprimée avec succès.', 'success')
        
        return jsonify({'redirect': url_for('pokedex.pokedex')})

    return bp
