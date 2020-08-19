from project_manager import db, login_manager
from datetime import datetime
from project_manager import migrate

# Adds required attributes and methods to our class
from flask_login import UserMixin

@login_manager.user_loader	
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20),unique=True,nullable=False)
	email = db.Column(db.String(120),unique=True,nullable=False)
	role = db.Column(db.String(100),unique=True,nullable=False)
	image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
	password = db.Column(db.String(60),nullable=False)
	project = db.relationship('Project',backref='manager',lazy=True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}','{self.role}')"


class Project(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(100),nullable=False)
	date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	description = db.Column(db.Text,nullable=False)
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	users = db.relationship('User',backref='developers',lazy=True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

	def __repr__(self):
		return f"Project('{self.title}','{self.date_added}')"


class Task(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	task_name = db.Column(db.String(100),nullable=False)
	date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	task_details = db.Column(db.Text,nullable=False)
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	status = db.Column(db.String(50),nullable=False)
	project_id = db.Column(db.Integer,db.ForeignKey('project.id'),nullable=False)
	developer = db.Column(db.String(100))
	
	def __repr__(self):
		return f"Task('{self.task_name}','{self.date_added}','{self.status}')"