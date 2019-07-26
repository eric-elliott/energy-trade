from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from soltrade.models import User, Group, Offer
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=22)])
    email = StringField('email', validators=[DataRequired(), Email()])
    group = SelectField('group', choices=[(g.groupname, g.groupname) for g in Group.query.order_by('groupname')], validators=[InputRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username has been taken --- please select another username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email has been taken --- please use another email.')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=22)])
    email = StringField('email', validators=[DataRequired(), Email()])
    pic = FileField('set profile picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username has been taken --- please select another username.')

    def validate_email(self, email):
        if email.data != current_user.email: 
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email has been taken --- please use another email.')

class OfferForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=2, max=100)])
    energy_offer = DecimalField('energy offer (kWh)', places=2, validators=[DataRequired()])
    submit = SubmitField("Post Offer")

    def validate_offer():
        if current_user.offers != None:
            raise ValidationError("You've already made an offer today!")



class RequestForm(FlaskForm):
    energy_requested = DecimalField('amount of energy requested (kWh)', places=2, validators=[DataRequired()])
    payment = DecimalField('maximum amount willing to pay ($)', places=2, validators=[DataRequired()])
    submit = SubmitField("Make Request")
