from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from project_manager.models import User



class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	role = StringField('Role',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired(),EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')

	# custom validation for unique emails
	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is Taken !')
	
	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is Taken !')


class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Login')
	

class ProjectForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired(),Length(min=3,max=25)])
	description = TextAreaField('Description',validators=[DataRequired()])
	start_date = DateField('Start Date',format='%Y-%m-%d',validators=[DataRequired()])
	end_date = DateField('Expected End Date',format='%Y-%m-%d',validators=[DataRequired()])
	submit = SubmitField('Submit Project')


class TaskForm(FlaskForm):
	users = User.query.all()
	username = []
	for user in users:
		username.append(user.username)

	username.insert(0,'None') 
	task_name = StringField('Task Name',validators=[DataRequired(),Length(min=5,max=50)])
	task_details = TextAreaField('Task Details',validators=[DataRequired()])
	start_date = DateField('Start Date',format='%Y-%m-%d',validators=[DataRequired()])
	end_date = DateField('Task End Date',format='%Y-%m-%d',validators=[DataRequired()])
	status = SelectField(u'Task Status', choices=[('not_started', 'Not Started'),('active', 'Active'),('completed', 'Completed')])
	developer = SelectField(u'Task Developer', choices=username)
	submit = SubmitField('Submit Task')

	# # custom validation for unique emails
	# def validate_username(self,username):
	# 	user = User.query.filter_by(username=username.data).first()
	# 	if user:
	# 		raise ValidationError('Username is Taken !')
	
	# def validate_email(self,email):
	# 	user = User.query.filter_by(email=email.data).first()
	# 	if user:
	# 		raise ValidationError('Email is Taken !')




# class UpdateAccountForm(FlaskForm):
# 	username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
# 	email = StringField('Email',validators=[DataRequired()])
# 	picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
# 	submit = SubmitField('Update')

# 	#custom validation for unique emails
# 	def validate_username(self,username):
# 		if username.data != current_user.username:
# 			user = User.query.filter_by(username=username.data).first()
# 			if user:
# 				raise ValidationError('Username is Taken.')
		
# 	def validate_email(self,email):
# 		if email.data != current_user.email:
# 			user = User.query.filter_by(email=email.data).first()
# 			if user:
# 				raise ValidationError('Email is Taken.')


# class RequestResetForm(FlaskForm):
# 	email = StringField('Email',validators=[DataRequired()])
# 	submit = SubmitField('Request Password Reset')

# 	def validate_email(self,email):

# 		user = User.query.filter_by(email=email.data).first()
# 		if user is None:
# 			raise ValidationError('Account not found with that email.')

# class ResetPasswordForm(FlaskForm):
# 	password = PasswordField('Password',validators=[DataRequired()])
# 	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
# 	submit = SubmitField('Reset Password')