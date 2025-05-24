from datetime import datetime
from app import db

class Team(db.Model):
    """IPL Team model."""
    _tablename_ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    home_ground = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(255))
    primary_color = db.Column(db.String(20))
    secondary_color = db.Column(db.String(20))
    championships_won = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    players = db.relationship('Player', backref='team', lazy=True)
    owners = db.relationship('TeamOwner', backref='team', lazy=True)
    sponsors = db.relationship('TeamSponsor', backref='team', lazy=True)
    home_matches = db.relationship('Match', foreign_keys='Match.home_team_id', backref='home_team', lazy=True)
    away_matches = db.relationship('Match', foreign_keys='Match.away_team_id', backref='away_team', lazy=True)
    
    def _repr_(self):
        return f'<Team {self.name}>'

class Player(db.Model):
    """IPL Player model."""
    _tablename_ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)
    batting_style = db.Column(db.String(50))
    bowling_style = db.Column(db.String(50))
    role = db.Column(db.String(50), nullable=False)  # Batsman, Bowler, All-rounder, Wicket-keeper
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    jersey_number = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stats = db.relationship('Stats', backref='player', lazy=True, uselist=False)
    runs_stats = db.relationship('RunsStats', backref='player', lazy=True, uselist=False)
    contract = db.relationship('ContractDetails', backref='player', lazy=True, uselist=False)
    
    def _repr_(self):
        return f'<Player {self.name}>'

class Match(db.Model):
    """IPL Match model."""
    _tablename_ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    match_date = db.Column(db.DateTime, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.id'), nullable=False)
    match_type = db.Column(db.String(50), default='League')  # League, Playoff, Final
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Live, Completed, Cancelled
    winner_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    man_of_match_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    home_team_score = db.Column(db.String(20), nullable=True)
    away_team_score = db.Column(db.String(20), nullable=True)
    match_summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stadium = db.relationship('Stadium', backref='matches')
    tickets = db.relationship('Ticket', backref='match', lazy=True)
    winner = db.relationship('Team', foreign_keys=[winner_id])
    man_of_match = db.relationship('Player', foreign_keys=[man_of_match_id])
    
    def _repr_(self):
        return f'<Match {self.home_team.name} vs {self.away_team.name} on {self.match_date}>'

class Stadium(db.Model):
    """Stadium model for IPL matches."""
    _tablename_ = 'stadium'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), default='India')
    capacity = db.Column(db.Integer, nullable=False)
    established_year = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<Stadium {self.name}>'

class Ticket(db.Model):
    """Ticket model for IPL matches."""
    _tablename_ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # VIP, Premium, Standard
    price = db.Column(db.Float, nullable=False)
    total_available = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, default=0)
    sale_start_date = db.Column(db.DateTime)
    sale_end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<Ticket {self.category} for Match {self.match_id}>'

class TeamOwner(db.Model):
    """Team Owners model."""
    _tablename_ = 'team_owners'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    ownership_percentage = db.Column(db.Float)
    year_acquired = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<TeamOwner {self.owner_name} of {self.team.name}>'

class TeamSponsor(db.Model):
    """Team Sponsors model."""
    _tablename_ = 'team_sponsor'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    sponsor_name = db.Column(db.String(100), nullable=False)
    sponsor_type = db.Column(db.String(50))  # Principal, Associate, Official
    deal_amount = db.Column(db.Float)
    deal_start_date = db.Column(db.Date)
    deal_end_date = db.Column(db.Date)
    logo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<TeamSponsor {self.sponsor_name} for {self.team.name}>'

class LeagueSponsor(db.Model):
    """IPL League Sponsors model."""
    _tablename_ = 'league_sponsor'
    
    id = db.Column(db.Integer, primary_key=True)
    sponsor_name = db.Column(db.String(100), nullable=False)
    sponsor_type = db.Column(db.String(50))  # Title, Associate, Official
    deal_amount = db.Column(db.Float)
    deal_start_date = db.Column(db.Date)
    deal_end_date = db.Column(db.Date)
    logo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<LeagueSponsor {self.sponsor_name}>'

class IPLCommittee(db.Model):
    """IPL Committee model."""
    _tablename_ = 'ipl_committee'
    
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    appointed_date = db.Column(db.Date)
    term_end_date = db.Column(db.Date)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<IPLCommittee {self.member_name}, {self.position}>'

class HeadCoach(db.Model):
    """Head Coach model for IPL teams."""
    _tablename_ = 'head_coach'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    appointed_date = db.Column(db.Date)
    contract_end_date = db.Column(db.Date)
    previous_experience = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team = db.relationship('Team', backref='head_coach', lazy=True, uselist=False)
    
    def _repr_(self):
        return f'<HeadCoach {self.name} of {self.team.name}>'

class ContractDetails(db.Model):
    """Player Contract Details model."""
    _tablename_ = 'contract_details'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    final_bid = db.Column(db.Float, nullable=False)
    contract_start_date = db.Column(db.Date)
    contract_end_date = db.Column(db.Date)
    retention_type = db.Column(db.String(50))  # New signing, Retained, RTM
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<ContractDetails for {self.player.name}>'

class Stats(db.Model):
    """Player Statistics model."""
    _tablename_ = 'stats'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    matches_played = db.Column(db.Integer, default=0)
    runs_scored = db.Column(db.Integer, default=0)
    wickets_taken = db.Column(db.Integer, default=0)
    highest_score = db.Column(db.Integer, default=0)
    best_bowling_figures = db.Column(db.String(20))
    batting_average = db.Column(db.Float, default=0.0)
    bowling_average = db.Column(db.Float, default=0.0)
    economy_rate = db.Column(db.Float, default=0.0)
    strike_rate = db.Column(db.Float, default=0.0)
    hundreds = db.Column(db.Integer, default=0)
    fifties = db.Column(db.Integer, default=0)
    fours = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<Stats for {self.player.name}>'

class RunsStats(db.Model):
    """Player Runs Statistics model for current season."""
    _tablename_ = 'runs_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    season_year = db.Column(db.Integer, default=2023)
    matches = db.Column(db.Integer, default=0)
    innings = db.Column(db.Integer, default=0)
    runs = db.Column(db.Integer, default=0)
    highest_score = db.Column(db.Integer, default=0)
    average = db.Column(db.Float, default=0.0)
    strike_rate = db.Column(db.Float, default=0.0)
    hundreds = db.Column(db.Integer, default=0)
    fifties = db.Column(db.Integer, default=0)
    fours = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<RunsStats for {self.player.name}, {self.season_year}>'

class OrangeCap(db.Model):
    """Orange Cap model for top run scorers."""
    _tablename_ = 'orange_cap'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    season_year = db.Column(db.Integer, default=2023)
    matches = db.Column(db.Integer, default=0)
    runs = db.Column(db.Integer, default=0)
    average = db.Column(db.Float, default=0.0)
    strike_rate = db.Column(db.Float, default=0.0)
    rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    player = db.relationship('Player', backref='orange_cap')
    
    def _repr_(self):
        return f'<OrangeCap {self.player.name}, Rank: {self.rank}>'

class PurpleCap(db.Model):
    """Purple Cap model for top wicket takers."""
    _tablename_ = 'purple_cap'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    season_year = db.Column(db.Integer, default=2023)
    matches = db.Column(db.Integer, default=0)
    wickets = db.Column(db.Integer, default=0)
    economy = db.Column(db.Float, default=0.0)
    average = db.Column(db.Float, default=0.0)
    rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    player = db.relationship('Player', backref='purple_cap')
    
    def _repr_(self):
        return f'<PurpleCap {self.player.name}, Rank: {self.rank}>'

routes.py

from flask import render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from app import app, db
from models import (Team, Player, Match, Stadium, Ticket, 
                   TeamOwner, TeamSponsor, LeagueSponsor, 
                   IPLCommittee, HeadCoach, ContractDetails, 
                   Stats, RunsStats, OrangeCap, PurpleCap)
from forms import (TeamForm, PlayerForm, MatchForm, StadiumForm, 
                  TicketForm, TeamOwnerForm, SponsorForm, 
                  HeadCoachForm, ContractDetailsForm, StatsForm)

# Frontend Routes
@app.route('/')
def index():
    """Home page with latest matches and standings."""
    # Get upcoming matches
    upcoming_matches = Match.query.filter(
        Match.match_date >= datetime.utcnow(),
        Match.status == 'Scheduled'
    ).order_by(Match.match_date).limit(5).all()
    
    # Get recent matches
    recent_matches = Match.query.filter(
        Match.status == 'Completed'
    ).order_by(Match.match_date.desc()).limit(5).all()
    
    # Get teams for standings
    teams = Team.query.all()
    # Sort teams by championships won (simple standings)
    teams.sort(key=lambda x: x.championships_won, reverse=True)
    
    # Get orange cap holders
    orange_cap = OrangeCap.query.order_by(OrangeCap.rank).limit(5).all()
    
    # Get purple cap holders
    purple_cap = PurpleCap.query.order_by(PurpleCap.rank).limit(5).all()
    
    return render_template('index.html', 
                          upcoming_matches=upcoming_matches,
                          recent_matches=recent_matches,
                          teams=teams,
                          orange_cap=orange_cap,
                          purple_cap=purple_cap)

@app.route('/teams')
def teams():
    """Teams listing page."""
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)

@app.route('/teams/<int:team_id>')
def team_details(team_id):
    """Team details page."""
    team = Team.query.get_or_404(team_id)
    players = Player.query.filter_by(team_id=team_id).all()
    coach = HeadCoach.query.filter_by(team_id=team_id).first()
    sponsors = TeamSponsor.query.filter_by(team_id=team_id).all()
    owners = TeamOwner.query.filter_by(team_id=team_id).all()
    
    # Get team's upcoming matches
    upcoming_matches = Match.query.filter(
        ((Match.home_team_id == team_id) | (Match.away_team_id == team_id)),
        Match.match_date >= datetime.utcnow(),
        Match.status == 'Scheduled'
    ).order_by(Match.match_date).limit(5).all()
    
    # Get team's recent matches
    recent_matches = Match.query.filter(
        ((Match.home_team_id == team_id) | (Match.away_team_id == team_id)),
        Match.status == 'Completed'
    ).order_by(Match.match_date.desc()).limit(5).all()
    
    return render_template('team_details.html', 
                          team=team,
                          players=players,
                          coach=coach,
                          sponsors=sponsors,
                          owners=owners,
                          upcoming_matches=upcoming_matches,
                          recent_matches=recent_matches)

@app.route('/players')
def players():
    """Players listing page."""
    players = Player.query.all()
    return render_template('players.html', players=players)

@app.route('/players/<int:player_id>')
def player_details(player_id):
    """Player details page."""
    player = Player.query.get_or_404(player_id)
    stats = Stats.query.filter_by(player_id=player_id).first()
    contract = ContractDetails.query.filter_by(player_id=player_id).first()
    
    # Check if player is in orange or purple cap
    orange_cap = OrangeCap.query.filter_by(player_id=player_id).first()
    purple_cap = PurpleCap.query.filter_by(player_id=player_id).first()
    
    return render_template('player_details.html', 
                          player=player,
                          stats=stats,
                          contract=contract,
                          orange_cap=orange_cap,
                          purple_cap=purple_cap)

@app.route('/matches')
def matches():
    """Matches listing page."""
    # Filter by status if provided
    status = request.args.get('status', 'all')
    
    if status != 'all':
        matches = Match.query.filter_by(status=status).order_by(Match.match_date).all()
    else:
        matches = Match.query.order_by(Match.match_date).all()
    
    return render_template('matches.html', matches=matches, current_filter=status)

@app.route('/matches/<int:match_id>')
def match_details(match_id):
    """Match details page."""
    match = Match.query.get_or_404(match_id)
    tickets = Ticket.query.filter_by(match_id=match_id).all()
    
    return render_template('match_details.html', match=match, tickets=tickets)

@app.route('/stats')
def stats():
    """Statistics page with orange and purple cap holders."""
    orange_cap = OrangeCap.query.order_by(OrangeCap.rank).all()
    purple_cap = PurpleCap.query.order_by(PurpleCap.rank).all()
    top_teams = sorted(Team.query.all(), key=lambda x: x.championships_won, reverse=True)[:5]
    
    return render_template('stats.html', 
                           orange_cap=orange_cap, 
                           purple_cap=purple_cap, 
                           top_teams=top_teams)

@app.route('/tickets')
def tickets():
    """Tickets listing page."""
    # Get upcoming matches with available tickets
    upcoming_matches = Match.query.filter(
        Match.match_date >= datetime.utcnow(),
        Match.status == 'Scheduled'
    ).order_by(Match.match_date).all()
    
    match_tickets = {}
    for match in upcoming_matches:
        tickets = Ticket.query.filter_by(match_id=match.id).all()
        if tickets:
            match_tickets[match.id] = tickets
    
    return render_template('tickets.html', 
                          upcoming_matches=upcoming_matches,
                          match_tickets=match_tickets)

@app.route('/sponsors')
def sponsors():
    """Sponsors listing page."""
    league_sponsors = LeagueSponsor.query.all()
    team_sponsors = TeamSponsor.query.all()
    teams = Team.query.all()
    
    return render_template('sponsors.html', 
                          league_sponsors=league_sponsors,
                          team_sponsors=team_sponsors,
                          teams=teams)

# Admin Routes
@app.route('/admin')
def admin_index():
    """Admin dashboard."""
    teams_count = Team.query.count()
    players_count = Player.query.count()
    matches_count = Match.query.count()
    stadiums_count = Stadium.query.count()
    sponsors_count = TeamSponsor.query.count() + LeagueSponsor.query.count()
    
    return render_template('admin/index.html',
                          teams_count=teams_count,
                          players_count=players_count,
                          matches_count=matches_count,
                          stadiums_count=stadiums_count,
                          sponsors_count=sponsors_count)

# Admin Team Routes
@app.route('/admin/teams')
def admin_teams():
    """Admin teams management."""
    teams = Team.query.all()
    return render_template('admin/teams.html', teams=teams)

@app.route('/admin/teams/add', methods=['GET', 'POST'])
def admin_add_team():
    """Add new team."""
    form = TeamForm()
    
    if form.validate_on_submit():
        team = Team(
            name=form.name.data,
            short_name=form.short_name.data,
            city=form.city.data,
            home_ground=form.home_ground.data,
            logo_url=form.logo_url.data,
            primary_color=form.primary_color.data,
            secondary_color=form.secondary_color.data,
            championships_won=form.championships_won.data
        )
        db.session.add(team)
        db.session.commit()
        flash('Team added successfully!', 'success')
        return redirect(url_for('admin_teams'))
    
    return render_template('admin/teams.html', form=form, teams=None)

@app.route('/admin/teams/edit/<int:team_id>', methods=['GET', 'POST'])
def admin_edit_team(team_id):
    """Edit existing team."""
    team = Team.query.get_or_404(team_id)
    form = TeamForm(obj=team)
    
    if form.validate_on_submit():
        form.populate_obj(team)
        db.session.commit()
        flash('Team updated successfully!', 'success')
        return redirect(url_for('admin_teams'))
    
    return render_template('admin/teams.html', form=form, teams=None, edit_id=team_id)

@app.route('/admin/teams/delete/<int:team_id>')
def admin_delete_team(team_id):
    """Delete team."""
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    flash('Team deleted successfully!', 'success')
    return redirect(url_for('admin_teams'))

# Admin Player Routes
@app.route('/admin/players')
def admin_players():
    """Admin players management."""
    players = Player.query.all()
    return render_template('admin/players.html', players=players)

@app.route('/admin/players/add', methods=['GET', 'POST'])
def admin_add_player():
    """Add new player."""
    form = PlayerForm()
    # Get team choices
    form.team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    
    if form.validate_on_submit():
        player = Player(
            name=form.name.data,
            country=form.country.data,
            date_of_birth=form.date_of_birth.data,
            batting_style=form.batting_style.data,
            bowling_style=form.bowling_style.data,
            role=form.role.data,
            team_id=form.team_id.data,
            jersey_number=form.jersey_number.data,
            image_url=form.image_url.data
        )
        db.session.add(player)
        db.session.commit()
        
        # Create empty stats record for the player
        stats = Stats(player_id=player.id)
        db.session.add(stats)
        db.session.commit()
        
        flash('Player added successfully!', 'success')
        return redirect(url_for('admin_players'))
    
    return render_template('admin/players.html', form=form, players=None)

@app.route('/admin/players/edit/<int:player_id>', methods=['GET', 'POST'])
def admin_edit_player(player_id):
    """Edit existing player."""
    player = Player.query.get_or_404(player_id)
    form = PlayerForm(obj=player)
    # Get team choices
    form.team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    
    if form.validate_on_submit():
        form.populate_obj(player)
        db.session.commit()
        flash('Player updated successfully!', 'success')
        return redirect(url_for('admin_players'))
    
    return render_template('admin/players.html', form=form, players=None, edit_id=player_id)

@app.route('/admin/players/delete/<int:player_id>')
def admin_delete_player(player_id):
    """Delete player."""
    player = Player.query.get_or_404(player_id)
    
    # Delete related records first
    stats = Stats.query.filter_by(player_id=player_id).first()
    if stats:
        db.session.delete(stats)
    
    contract = ContractDetails.query.filter_by(player_id=player_id).first()
    if contract:
        db.session.delete(contract)
    
    orange_cap = OrangeCap.query.filter_by(player_id=player_id).first()
    if orange_cap:
        db.session.delete(orange_cap)
    
    purple_cap = PurpleCap.query.filter_by(player_id=player_id).first()
    if purple_cap:
        db.session.delete(purple_cap)
    
    db.session.delete(player)
    db.session.commit()
    flash('Player deleted successfully!', 'success')
    return redirect(url_for('admin_players'))

@app.route('/admin/players/stats/<int:player_id>', methods=['GET', 'POST'])
def admin_player_stats(player_id):
    """Edit player statistics."""
    player = Player.query.get_or_404(player_id)
    stats = Stats.query.filter_by(player_id=player_id).first()
    
    if not stats:
        stats = Stats(player_id=player_id)
        db.session.add(stats)
        db.session.commit()
    
    form = StatsForm(obj=stats)
    
    if form.validate_on_submit():
        form.populate_obj(stats)
        db.session.commit()
        flash('Player statistics updated successfully!', 'success')
        return redirect(url_for('admin_players'))
    
    return render_template('admin/players.html', stats_form=form, player=player, players=None)

# Admin Match Routes
@app.route('/admin/matches')
def admin_matches():
    """Admin matches management."""
    matches = Match.query.all()
    return render_template('admin/matches.html', matches=matches)

@app.route('/admin/matches/add', methods=['GET', 'POST'])
def admin_add_match():
    """Add new match."""
    form = MatchForm()
    # Get choices for select fields
    form.home_team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    form.away_team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    form.stadium_id.choices = [(stadium.id, stadium.name) for stadium in Stadium.query.all()]
    form.winner_id.choices = [(team.id, team.name) for team in Team.query.all()]
    form.man_of_match_id.choices = [(player.id, player.name) for player in Player.query.all()]
    
    if form.validate_on_submit():
        # Validate home and away teams are different
        if form.home_team_id.data == form.away_team_id.data:
            flash('Home and away teams cannot be the same!', 'danger')
            return render_template('admin/matches.html', form=form, matches=None)
        
        match = Match(
            match_date=form.match_date.data,
            home_team_id=form.home_team_id.data,
            away_team_id=form.away_team_id.data,
            stadium_id=form.stadium_id.data,
            match_type=form.match_type.data,
            status=form.status.data,
            winner_id=form.winner_id.data if form.winner_id.data != 0 else None,
            man_of_match_id=form.man_of_match_id.data if form.man_of_match_id.data != 0 else None,
            home_team_score=form.home_team_score.data,
            away_team_score=form.away_team_score.data,
            match_summary=form.match_summary.data
        )
        db.session.add(match)
        db.session.commit()
        flash('Match added successfully!', 'success')
        return redirect(url_for('admin_matches'))
    
    return render_template('admin/matches.html', form=form, matches=None)

@app.route('/admin/matches/edit/<int:match_id>', methods=['GET', 'POST'])
def admin_edit_match(match_id):
    """Edit existing match."""
    match = Match.query.get_or_404(match_id)
    form = MatchForm(obj=match)
    # Get choices for select fields
    form.home_team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    form.away_team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    form.stadium_id.choices = [(stadium.id, stadium.name) for stadium in Stadium.query.all()]
    form.winner_id.choices = [(team.id, team.name) for team in Team.query.all()]
    form.man_of_match_id.choices = [(player.id, player.name) for player in Player.query.all()]
    
    if form.validate_on_submit():
        # Validate home and away teams are different
        if form.home_team_id.data == form.away_team_id.data:
            flash('Home and away teams cannot be the same!', 'danger')
            return render_template('admin/matches.html', form=form, matches=None, edit_id=match_id)
        
        form.populate_obj(match)
        # Handle optional fields
        match.winner_id = form.winner_id.data if form.winner_id.data != 0 else None
        match.man_of_match_id = form.man_of_match_id.data if form.man_of_match_id.data != 0 else None
        
        db.session.commit()
        flash('Match updated successfully!', 'success')
        return redirect(url_for('admin_matches'))
    
    return render_template('admin/matches.html', form=form, matches=None, edit_id=match_id)

@app.route('/admin/matches/delete/<int:match_id>')
def admin_delete_match(match_id):
    """Delete match."""
    match = Match.query.get_or_404(match_id)
    
    # Delete related tickets first
    tickets = Ticket.query.filter_by(match_id=match_id).all()
    for ticket in tickets:
        db.session.delete(ticket)
    
    db.session.delete(match)
    db.session.commit()
    flash('Match deleted successfully!', 'success')
    return redirect(url_for('admin_matches'))

# Admin Stadium Routes
@app.route('/admin/stadiums')
def admin_stadiums():
    """Admin stadiums management."""
    stadiums = Stadium.query.all()
    return render_template('admin/stadiums.html', stadiums=stadiums)

@app.route('/admin/stadiums/add', methods=['GET', 'POST'])
def admin_add_stadium():
    """Add new stadium."""
    form = StadiumForm()
    
    if form.validate_on_submit():
        stadium = Stadium(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            country=form.country.data,
            capacity=form.capacity.data,
            established_year=form.established_year.data,
            image_url=form.image_url.data,
            description=form.description.data
        )
        db.session.add(stadium)
        db.session.commit()
        flash('Stadium added successfully!', 'success')
        return redirect(url_for('admin_stadiums'))
    
    return render_template('admin/stadiums.html', form=form, stadiums=None)

@app.route('/admin/stadiums/edit/<int:stadium_id>', methods=['GET', 'POST'])
def admin_edit_stadium(stadium_id):
    """Edit existing stadium."""
    stadium = Stadium.query.get_or_404(stadium_id)
    form = StadiumForm(obj=stadium)
    
    if form.validate_on_submit():
        form.populate_obj(stadium)
        db.session.commit()
        flash('Stadium updated successfully!', 'success')
        return redirect(url_for('admin_stadiums'))
    
    return render_template('admin/stadiums.html', form=form, stadiums=None, edit_id=stadium_id)

@app.route('/admin/stadiums/delete/<int:stadium_id>')
def admin_delete_stadium(stadium_id):
    """Delete stadium."""
    stadium = Stadium.query.get_or_404(stadium_id)
    
    # Check if stadium is referenced in any matches
    matches = Match.query.filter_by(stadium_id=stadium_id).first()
    if matches:
        flash('Cannot delete stadium as it is referenced in matches!', 'danger')
        return redirect(url_for('admin_stadiums'))
    
    db.session.delete(stadium)
    db.session.commit()
    flash('Stadium deleted successfully!', 'success')
    return redirect(url_for('admin_stadiums'))

# Admin Ticket Routes
@app.route('/admin/tickets')
def admin_tickets():
    """Admin tickets management."""
    tickets = Ticket.query.all()
    return render_template('admin/tickets.html', tickets=tickets)

@app.route('/admin/tickets/add', methods=['GET', 'POST'])
def admin_add_ticket():
    """Add new ticket."""
    form = TicketForm()
    # Get match choices
    upcoming_matches = Match.query.filter(
        Match.match_date >= datetime.utcnow(),
        Match.status == 'Scheduled'
    ).order_by(Match.match_date).all()
    
    form.match_id.choices = [(match.id, f"{match.home_team.name} vs {match.away_team.name} on {match.match_date.strftime('%d-%m-%Y')}") for match in upcoming_matches]
    
    if form.validate_on_submit():
        ticket = Ticket(
            match_id=form.match_id.data,
            category=form.category.data,
            price=form.price.data,
            total_available=form.total_available.data,
            sale_start_date=form.sale_start_date.data,
            sale_end_date=form.sale_end_date.data
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket added successfully!', 'success')
        return redirect(url_for('admin_tickets'))
    
    return render_template('admin/tickets.html', form=form, tickets=None)

@app.route('/admin/tickets/edit/<int:ticket_id>', methods=['GET', 'POST'])
def admin_edit_ticket(ticket_id):
    """Edit existing ticket."""
    ticket = Ticket.query.get_or_404(ticket_id)
    form = TicketForm(obj=ticket)
    
    # Get match choices
    upcoming_matches = Match.query.filter(
        Match.match_date >= datetime.utcnow(),
        Match.status == 'Scheduled'
    ).order_by(Match.match_date).all()
    
    form.match_id.choices = [(match.id, f"{match.home_team.name} vs {match.away_team.name} on {match.match_date.strftime('%d-%m-%Y')}") for match in upcoming_matches]
    
    # Add current match as a choice even if it's in the past
    match = Match.query.get(ticket.match_id)
    if match and match not in upcoming_matches:
        form.match_id.choices.append((match.id, f"{match.home_team.name} vs {match.away_team.name} on {match.match_date.strftime('%d-%m-%Y')} (Past)"))
    
    if form.validate_on_submit():
        form.populate_obj(ticket)
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('admin_tickets'))
    
    return render_template('admin/tickets.html', form=form, tickets=None, edit_id=ticket_id)

@app.route('/admin/tickets/delete/<int:ticket_id>')
def admin_delete_ticket(ticket_id):
    """Delete ticket."""
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully!', 'success')
    return redirect(url_for('admin_tickets'))

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Load data for testing (can be removed in production)
@app.route('/populate-test-data')
def populate_test_data():
    """Populate test data for development purposes."""
    # Add teams
    if Team.query.count() == 0:
        teams = [
            {'name': 'Mumbai Indians', 'short_name': 'MI', 'city': 'Mumbai', 'home_ground': 'Wankhede Stadium', 
             'primary_color': '#004BA0', 'secondary_color': '#D1AB3E', 'championships_won': 5},
            {'name': 'Chennai Super Kings', 'short_name': 'CSK', 'city': 'Chennai', 'home_ground': 'M.A. Chidambaram Stadium', 
             'primary_color': '#F9CD05', 'secondary_color': '#0081E5', 'championships_won': 4},
            {'name': 'Royal Challengers Bangalore', 'short_name': 'RCB', 'city': 'Bangalore', 'home_ground': 'M. Chinnaswamy Stadium', 
             'primary_color': '#EC1C24', 'secondary_color': '#000000', 'championships_won': 0},
        ]
        
        for team_data in teams:
            team = Team(**team_data)
            db.session.add(team)
        
        db.session.commit()
        
        # Add stadiums
        stadiums = [
            {'name': 'Wankhede Stadium', 'city': 'Mumbai', 'state': 'Maharashtra', 'capacity': 33000, 'established_year': 1974},
            {'name': 'M.A. Chidambaram Stadium', 'city': 'Chennai', 'state': 'Tamil Nadu', 'capacity': 50000, 'established_year': 1916},
            {'name': 'M. Chinnaswamy Stadium', 'city': 'Bangalore', 'state': 'Karnataka', 'capacity': 40000, 'established_year': 1969},
        ]
        
        for stadium_data in stadiums:
            stadium = Stadium(**stadium_data)
            db.session.add(stadium)
        
        db.session.commit()
        
        # Add a few players
        players_data = [
            {'name': 'Rohit Sharma', 'country': 'India', 'date_of_birth': datetime(1987, 4, 30), 
             'batting_style': 'Right-handed', 'role': 'Batsman', 'team_id': 1, 'jersey_number': 45},
            {'name': 'MS Dhoni', 'country': 'India', 'date_of_birth': datetime(1981, 7, 7), 
             'batting_style': 'Right-handed', 'role': 'Wicket-keeper', 'team_id': 2, 'jersey_number': 7},
            {'name': 'Virat Kohli', 'country': 'India', 'date_of_birth': datetime(1988, 11, 5), 
             'batting_style': 'Right-handed', 'role': 'Batsman', 'team_id': 3, 'jersey_number': 18},
        ]
        
        for player_data in players_data:
            player = Player(**player_data)
            db.session.add(player)
        
        db.session.commit()
        
        # Add matches
        matches_data = [
            {'match_date': datetime(2023, 4, 10, 19, 30), 'home_team_id': 1, 'away_team_id': 2, 'stadium_id': 1, 
             'status': 'Completed', 'home_team_score': '213/4', 'away_team_score': '206/7', 'winner_id': 1},
            {'match_date': datetime(2023, 4, 15, 19, 30), 'home_team_id': 3, 'away_team_id': 1, 'stadium_id': 3, 
             'status': 'Completed', 'home_team_score': '189/5', 'away_team_score': '192/3', 'winner_id': 1},
            {'match_date': datetime.utcnow() + (datetime(2023, 5, 1) - datetime(2023, 4, 20)), 
             'home_team_id': 2, 'away_team_id': 3, 'stadium_id': 2, 'status': 'Scheduled'},
        ]
        
        for match_data in matches_data:
            match = Match(**match_data)
            db.session.add(match)
        
        db.session.commit()
        
        # Add stats for players
        for i in range(1, 4):
            stats = Stats(
                player_id=i,
                matches_played=100,
                runs_scored=3000 + i*500,
                wickets_taken=5,
                highest_score=100 + i*10,
                batting_average=35.5 + i*2,
                strike_rate=140 + i*5
            )
            db.session.add(stats)
        
        # Add orange cap entries
        for i in range(1, 4):
            orange = OrangeCap(
                player_id=i,
                runs=500 + (3-i)*100,
                average=40 + (3-i)*5,
                strike_rate=150 + (3-i)*2,
                rank=i
            )
            db.session.add(orange)
        
        db.session.commit()
        
        # Add tickets for upcoming match
        upcoming_match = Match.query.filter_by(status='Scheduled').first()
        if upcoming_match:
            ticket_categories = ['VIP', 'Premium', 'Standard']
            prices = [10000, 5000, 2000]
            
            for i, category in enumerate(ticket_categories):
                ticket = Ticket(
                    match_id=upcoming_match.id,
                    category=category,
                    price=prices[i],
                    total_available=1000,
                    sale_start_date=datetime.utcnow(),
                    sale_end_date=upcoming_match.match_date
                )
                db.session.add(ticket)
            
            db.session.commit()
        
        # Add sponsors
        league_sponsor = LeagueSponsor(
            sponsor_name="TATA",
            sponsor_type="Title",
            deal_amount=500.0,
            deal_start_date=datetime(2023, 3, 1),
            deal_end_date=datetime(2023, 6, 30)
        )
        db.session.add(league_sponsor)
        
        for i in range(1, 4):
            team_sponsor = TeamSponsor(
                team_id=i,
                sponsor_name=f"Sponsor {i}",
                sponsor_type="Principal",
                deal_amount=50.0 + i*10,
                deal_start_date=datetime(2023, 3, 1),
                deal_end_date=datetime(2023, 6, 30)
            )
            db.session.add(team_sponsor)
        
        db.session.commit()
        
        flash('Test data populated successfully!', 'success')
    else:
        flash('Test data already exists!', 'info')
    
    return redirect(url_for('index'))
