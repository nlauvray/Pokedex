from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from models import db
from models.users import User
from models.model_pokemon import Pokemon
from models.teams import Team
from systems.auth import AuthSystem

def get_routes():
    bp = Blueprint('teams', __name__, url_prefix='/teams')

    # Route pour créer une équipe
    @bp.route('/create', methods=['GET', 'POST'])
    @AuthSystem.login_required
    def create_team():
        user = User.query.get(session['user_id'])
        pokemons = Pokemon.query.all()
        if request.method == 'POST':
            team_name = request.form['team_name']
            selected_pokemons = request.form.getlist('pokemons')
            new_team = Team(name=team_name, trainer_id=user.id)
            db.session.add(new_team)
            db.session.commit()
            for pokemon_id in selected_pokemons:
                pokemon = Pokemon.query.get(pokemon_id)
                new_team.pokemons.append(pokemon)
            db.session.commit()
            return redirect(url_for('teams.team', team_id=new_team.id))
        return render_template('create_team.html', user=user, pokemons=pokemons)

    # Route pour supprimer une équipe
    @bp.route('/<int:team_id>', methods=['DELETE', 'GET'])
    @AuthSystem.login_required
    def team(team_id):
        if request.method == 'GET':
            team = Team.query.get_or_404(team_id)
            return render_template('team.html', team=team)
        else:
            team = Team.query.get_or_404(team_id)
            if team.trainer_id != session['user_id']:
                flash('Vous n\'êtes pas autorisé à supprimer cette équipe.', 'danger')
                return redirect(url_for('pokedex.pokedex'))
            db.session.delete(team)
            db.session.commit()
            flash('Équipe supprimée avec succès.', 'success')
            return redirect(url_for('pokedex.pokedex'))

    return bp
