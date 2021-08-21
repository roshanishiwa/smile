from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length,Email
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.models import Post, Tag, User

def get_tags():
	return Tag.query

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    submit = SubmitField('Post')
    body = TextAreaField('Post Message', validators=[DataRequired(), Length(max=1500)])
    tag = QuerySelectMultipleField('Tag', query_factory=get_tags, get_label='name', widget=ListWidget(prefix_label=False),
    	option_widget=CheckboxInput())

class SortForm(FlaskForm):
	sort = SelectField('Sort By:', choices = [(1, 'Date'), (2, 'Title'), (3,'# of likes'), (4, 'Happiness Level')])
	refresh = SubmitField('Refresh')
	select = BooleanField('Display my posts only')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), 
		EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('The username aready exists. Please choose a different username!')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None: 
			raise ValidationError('The email aready exists. Please use a different email address!')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


