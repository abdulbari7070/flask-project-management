from flask import render_template, url_for, flash, redirect, request
from project_manager.forms import RegistrationForm, LoginForm, ProjectForm, TaskForm
from project_manager.models import User,Project,Task
from project_manager import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

projects = [
{
	'title':'Avataar Generation',
	'description':'Create Avataar from users image'
},
{
	'title':'Smart Sthethoscope',
	'description':'Create Avataar from users image'
},
{
	'title':'Avataar Generation',
	'description':'Create Avataar from users image'
}
]


@app.route("/")
@app.route("/home")
def home():
	projects = Project.query.order_by(Project.start_date.desc())
	current_date = datetime.utcnow()
	# projects.append('current_date',datetime.utcnow)
	print(current_date)
	return render_template('home.html', title='Homepage',projects=projects,current_date=current_date)


@app.route("/about")
def about():
	return render_template('about.html',title='About')


@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data,):
			login_user(user)
			flash('Login successful !','success')
			return redirect(url_for('home'))
		else:
			flash('Login unsuccessful ! Please check email and password.','warning')
	return render_template('login.html',title='Login', form=form)


@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,email=form.email.data,role=form.role.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created !','success')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/project/new", methods=['GET','POST'])
@login_required
def add_project():
	form = ProjectForm()
	if form.validate_on_submit():
		# print(current_user.id)
		project = Project(title=form.title.data,description=form.description.data,start_date=form.start_date.data,end_date=form.end_date.data,user_id=current_user.id)
		db.session.add(project)
		db.session.commit()
		flash('Project added successfully !','success')
		return redirect(url_for('home'))
	return render_template('add_project.html',title='Add Project',form=form, legend='Add New Project')

@app.route("/project/<int:project_id>")
def project(project_id):
	project = Project.query.get_or_404(project_id)
	tasks = Task.query.filter_by(project_id=project_id).order_by(Task.date_added.desc())
	return render_template('project.html',title=project.title,project=project,tasks=tasks)


@app.route("/project/<int:project_id>/update",methods=['GET','POST'])
@login_required
def update_project(project_id):
	project = Project.query.get_or_404(project_id)
	if project.manager != current_user:
		abort(403)
	form = ProjectForm()
	if form.validate_on_submit():
		project.title = form.title.data
		project.description = form.description.data
		project.start_date = form.start_date.data
		project.end_date = form.end_date.data
		db.session.commit()
		flash('Your project has been updated !','success')
		return redirect(url_for('project',project_id=project.id))
	elif request.method == 'GET':
		form.title.data = project.title
		form.description.data = project.description
		form.start_date.data = project.start_date
		form.end_date.data = project.end_date
	return render_template('add_project.html',title='Update Project',form=form, legend='Update Project')

@app.route("/project/<int:project_id>/delete",methods=['POST'])
@login_required
def delete_project(project_id):
	project = Project.query.get_or_404(project_id)
	if project.manager != current_user:
		abort(403)
	db.session.delete(project)
	db.session.commit()
	flash('Your project has been deleted !','success')
	return redirect(url_for('home'))


@app.route("/project/<int:project_id>/add_task",methods=['GET','POST'])
@login_required
def add_task(project_id):
	project = Project.query.get_or_404(project_id)
	if project.manager != current_user:
		abort(403)
	form = TaskForm()
	if form.validate_on_submit():
		task = Task(project_id=project_id,task_name=form.task_name.data,task_details=form.task_details.data,start_date=form.start_date.data,end_date=form.end_date.data,status=form.status.data)
		db.session.add(task)
		db.session.commit()
		flash('Task added successfully !','success')
		return redirect(url_for('project',project_id=project.id))
	return render_template('add_task.html',title='Add Task',legend='Add Task',form=form,project=project)


@app.route("/project/<int:project_id>/update_task/<int:task_id>",methods=['GET','POST'])
@login_required
def update_task(project_id,task_id):
	task = Task.query.get_or_404(task_id)
	project = Project.query.get_or_404(project_id)
	if project.manager != current_user:
		abort(403)
	form = TaskForm()
	if request.method == 'POST':		
		if form.validate_on_submit():
			task.task_name = form.task_name.data
			task.task_details = form.task_details.data
			task.start_date = form.start_date.data
			task.end_date = form.end_date.data
			task.status = form.status.data
			task.developer = form.developer.data
			db.session.commit()
			flash('Your task has been updated !','success')
			return redirect(url_for('project',project_id=project.id))
	elif request.method == 'GET':
		form.task_name.data = task.task_name
		form.task_details.data = task.task_details
		form.start_date.data = task.start_date
		form.end_date.data = task.end_date
		form.status.data = task.status
		form.developer.data = task.developer
	return render_template('add_task.html',title='Update Task',legend='Update Task',form=form,project=project,task=task)



# @app.route("/projects", methods=['GET','POST'])
# def projects():
# 	form = ProjectForm()
# 	if form.validate_on_submit():
# 		projects = Project.query.all()
# 		if user and bcrypt.check_password_hash(user.password,form.password.data,):
# 			login_user(user)
# 			flash('Login successful !','success')
# 			return redirect(url_for('home'))
# 		else:
# 			flash('Login unsuccessful ! Please check email and password.','warning')
# 	return render_template('login.html',title='Login', form=form)