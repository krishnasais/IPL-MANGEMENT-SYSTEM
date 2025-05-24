from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, DateField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional, Length, NumberRange

class TeamForm(FlaskForm):
    """Form for creating and editing teams"""
    name = StringField('Team Name', validators=[DataRequired(), Length(max=100)])
    short_name = StringField('Short Name', validators=[DataRequired(), Length(max=10)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    home_ground = StringField('Home Ground', validators=[DataRequired(), Length(max=100)])
    logo_url = StringField('Logo URL', validators=[Length(max=255)])
    primary_color = StringField('Primary Color', validators=[Length(max=20)])
    secondary_color = StringField('Secondary Color', validators=[Length(max=20)])
    championships_won = IntegerField('Championships Won', validators=[NumberRange(min=0)], default=0)
    submit = SubmitField('Submit')

class PlayerForm(FlaskForm):
    """Form for creating and editing players"""
    name = StringField('Player Name', validators=[DataRequired(), Length(max=100)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    batting_style = StringField('Batting Style', validators=[Length(max=50)])
    bowling_style = StringField('Bowling Style', validators=[Length(max=50)])
    role = SelectField('Role', choices=[
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All-rounder', 'All-rounder'),
        ('Wicket-keeper', 'Wicket-keeper')
    ], validators=[DataRequired()])
    team_id = SelectField('Team', validators=[DataRequired()], coerce=int)
    jersey_number = IntegerField('Jersey Number', validators=[Optional()])
    image_url = StringField('Image URL', validators=[Length(max=255)])
    submit = SubmitField('Submit')

class MatchForm(FlaskForm):
    """Form for creating and editing matches"""
    match_date = DateField('Match Date', validators=[DataRequired()])
    home_team_id = SelectField('Home Team', validators=[DataRequired()], coerce=int)
    away_team_id = SelectField('Away Team', validators=[DataRequired()], coerce=int)
    stadium_id = SelectField('Stadium', validators=[DataRequired()], coerce=int)
    match_type = SelectField('Match Type', choices=[
        ('League', 'League'),
        ('Playoff', 'Playoff'),
        ('Final', 'Final')
    ], validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Scheduled', 'Scheduled'),
        ('Live', 'Live'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    winner_id = SelectField('Winner', validators=[Optional()], coerce=int)
    man_of_match_id = SelectField('Man of the Match', validators=[Optional()], coerce=int)
    home_team_score = StringField('Home Team Score', validators=[Length(max=20)])
    away_team_score = StringField('Away Team Score', validators=[Length(max=20)])
    match_summary = TextAreaField('Match Summary')
    submit = SubmitField('Submit')
    
    def _init_(self, *args, **kwargs):
        super(MatchForm, self)._init_(*args, **kwargs)
        # Add empty choice for optional fields
        self.winner_id.choices.insert(0, (0, 'Select Winner'))
        self.man_of_match_id.choices.insert(0, (0, 'Select Man of the Match'))

class StadiumForm(FlaskForm):
    """Form for creating and editing stadiums"""
    name = StringField('Stadium Name', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)], default='India')
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1)])
    established_year = IntegerField('Established Year', validators=[Optional()])
    image_url = StringField('Image URL', validators=[Length(max=255)])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class TicketForm(FlaskForm):
    """Form for creating and editing tickets"""
    match_id = SelectField('Match', validators=[DataRequired()], coerce=int)
    category = SelectField('Category', choices=[
        ('VIP', 'VIP'),
        ('Premium', 'Premium'),
        ('Standard', 'Standard')
    ], validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    total_available = IntegerField('Total Available', validators=[DataRequired(), NumberRange(min=1)])
    sale_start_date = DateField('Sale Start Date', validators=[DataRequired()])
    sale_end_date = DateField('Sale End Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TeamOwnerForm(FlaskForm):
    """Form for creating and editing team owners"""
    team_id = SelectField('Team', validators=[DataRequired()], coerce=int)
    owner_name = StringField('Owner Name', validators=[DataRequired(), Length(max=100)])
    company = StringField('Company', validators=[DataRequired(), Length(max=100)])
    ownership_percentage = FloatField('Ownership Percentage', validators=[Optional(), NumberRange(min=0, max=100)])
    year_acquired = IntegerField('Year Acquired', validators=[Optional()])
    submit = SubmitField('Submit')

class SponsorForm(FlaskForm):
    """Form for creating and editing sponsors"""
    team_id = SelectField('Team', validators=[Optional()], coerce=int)
    sponsor_name = StringField('Sponsor Name', validators=[DataRequired(), Length(max=100)])
    sponsor_type = SelectField('Sponsor Type', choices=[
        ('Principal', 'Principal'),
        ('Associate', 'Associate'),
        ('Official', 'Official'),
        ('Title', 'Title')
    ], validators=[DataRequired()])
    deal_amount = FloatField('Deal Amount (in Crores)', validators=[Optional(), NumberRange(min=0)])
    deal_start_date = DateField('Deal Start Date', validators=[DataRequired()])
    deal_end_date = DateField('Deal End Date', validators=[DataRequired()])
    logo_url = StringField('Logo URL', validators=[Length(max=255)])
    submit = SubmitField('Submit')
    
    def _init_(self, *args, **kwargs):
        super(SponsorForm, self)._init_(*args, **kwargs)
        # Add empty choice for team field (for league sponsors)
        self.team_id.choices.insert(0, (0, 'League Sponsor (No Team)'))

class HeadCoachForm(FlaskForm):
    """Form for creating and editing head coaches"""
    team_id = SelectField('Team', validators=[DataRequired()], coerce=int)
    name = StringField('Coach Name', validators=[DataRequired(), Length(max=100)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    appointed_date = DateField('Appointed Date', validators=[DataRequired()])
    contract_end_date = DateField('Contract End Date', validators=[DataRequired()])
    previous_experience = TextAreaField('Previous Experience')
    submit = SubmitField('Submit')

class ContractDetailsForm(FlaskForm):
    """Form for creating and editing player contracts"""
    player_id = SelectField('Player', validators=[DataRequired()], coerce=int)
    base_price = FloatField('Base Price (in Crores)', validators=[DataRequired(), NumberRange(min=0)])
    final_bid = FloatField('Final Bid (in Crores)', validators=[DataRequired(), NumberRange(min=0)])
    contract_start_date = DateField('Contract Start Date', validators=[DataRequired()])
    contract_end_date = DateField('Contract End Date', validators=[DataRequired()])
    retention_type = SelectField('Retention Type', choices=[
        ('New signing', 'New signing'),
        ('Retained', 'Retained'),
        ('RTM', 'Right To Match (RTM)')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')

class StatsForm(FlaskForm):
    """Form for updating player statistics"""
    player_id = HiddenField('Player ID')
    matches_played = IntegerField('Matches Played', validators=[NumberRange(min=0)], default=0)
    runs_scored = IntegerField('Runs Scored', validators=[NumberRange(min=0)], default=0)
    wickets_taken = IntegerField('Wickets Taken', validators=[NumberRange(min=0)], default=0)
    highest_score = IntegerField('Highest Score', validators=[NumberRange(min=0)], default=0)
    best_bowling_figures = StringField('Best Bowling Figures', validators=[Length(max=20)])
    batting_average = FloatField('Batting Average', validators=[NumberRange(min=0)], default=0.0)
    bowling_average = FloatField('Bowling Average', validators=[NumberRange(min=0)], default=0.0)
    economy_rate = FloatField('Economy Rate', validators=[NumberRange(min=0)], default=0.0)
    strike_rate = FloatField('Strike Rate', validators=[NumberRange(min=0)], default=0.0)
    hundreds = IntegerField('Hundreds', validators=[NumberRange(min=0)], default=0)
    fifties = IntegerField('Fifties', validators=[NumberRange(min=0)], default=0)
    fours = IntegerField('Fours', validators=[NumberRange(min=0)], default=0)
    sixes = IntegerField('Sixes', validators=[NumberRange(min=0)], default=0)
    submit = SubmitField('Update Stats')

