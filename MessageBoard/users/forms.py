from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_login import current_user
from MessageBoard.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(), 
										Length(
												min=2, 
												max=20, 
												message="Usernames must have a minumum length of two characters and a maximum of twenty characters"
												)
										])
	email = StringField('Email', 
							validators=[DataRequired(), 
										Email(),
										Regexp(
												'^(\w+)(@)(spotx.tv)',
												message="You can only sign up with your Spotx email.")
										])
	password = PasswordField('Password', 
							validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
							validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email address is already in use here. Please register with a different one')


class LoginForm(FlaskForm):
	email = StringField('Email', 
						validators=[DataRequired(),Email()])
	password = PasswordField('Password', 
						validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', 
							validators=[
								DataRequired(), 
								Email(),
								Regexp('^(\w+)(@)(spotx.tv)', 
									message="Please use your'@spotx.tv' email address.")
								])
	picture = FileField('Change Profile Picture', 
							validators=[FileAllowed(['gif', 'jpeg', 'png'])])
	submit = SubmitField('Update Details')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Current username does not match.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Current email address does not match.')


class RequestResetForm(FlaskForm):
	email = StringField('Email', 
							validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('This account does not currently exist. Please register first.')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', 
							validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
							validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')


