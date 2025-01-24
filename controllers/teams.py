import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify
from models import db
from models.users import User
from models.pokemon import Pokemon
from models.teams import Team
from models.team_Pokemon import TeamPokemon
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
            selected_pokemons = request.form.getlist('pokemons')
            
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
        
        return render_template('team.html', team=team, all_pokemons=all_pokemons, team_pokemons=team_pokemons)

    # Route pour ajouter un Pokémon à une équipe
    @bp.route('/<int:team_id>/add_pokemon', methods=['POST'])
    @AuthSystem.login_required
    def add_pokemon_to_team(team_id):
        team = Team.query.get_or_404(team_id)
        pokemon_id = request.json.get('pokemon_id')
        pokemon = Pokemon.query.get(pokemon_id)
        
        if pokemon:
            existing_team_pokemon = TeamPokemon.query.filter_by(team_id=team.id, pokemon_id=pokemon.id).first()
            if not existing_team_pokemon:
                if len(team.pokemons) < 5:
                    team_pokemon = TeamPokemon(team_id=team.id, pokemon_id=pokemon.id)
                    db.session.add(team_pokemon)
                    db.session.commit()
                    
                    return jsonify({'success': True})
                
                else:
                    return jsonify({'success': False, 'error': 'L\'équipe a déjà 5 Pokémon.'})
            else:
                return jsonify({'success': False, 'error': 'Le Pokémon est déjà dans l\'équipe.'})
        else:
            return jsonify({'success': False, 'error': 'Pokémon non trouvé'})

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