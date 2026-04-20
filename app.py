from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from func import check_file, del_file
from db import *
from functools import wraps
from flask_login import (LoginManager, login_user, logout_user, 
	login_required, current_user)
from user import *
from forms import LoginForm

app = Flask(__name__, template_folder="templates")
app.debug = True
db = DataBase()

app.config['SECRET_KEY'] = 'ghj'
app.config['UPLOAD_FOLDER'] = 'static/images/'  # папка картинок

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(username):
	return User.get(username)

@app.route('/')
def index():
	return render_template("pages/index.html")

@app.route('/projects')
def projects():
	all_projects = db.select_all()
	return render_template("pages/projects.html", projects=all_projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('adminproject'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.authenticate(form.username.data, form.password.data)
		if user :
			login_user(user)
			return redirect(url_for('adminproject'))
		flash(['неверный логин или пароль', 'red'])
	return render_template("pages/login.html",form=form)

@app.route('/about')
def about():
	return render_template("pages/about.html")

@app.route('/admin_project', methods=['GET','POST'])
def adminproject():
	if request.method == "POST":
		if request.form.get("action") == 'delete':
			del_file(db.get_photo_id(request.form['id']))
			db.delete_project(request.form['id'])
		elif request.form.get("action") == 'update':
			if not request.files['image']:
				filename = db.get_photo_id(request.form['id'])
			else:
				file = request.files['image']
				del_file(db.get_photo_id(request.form['id']))
				if check_file(file.filename):
					filename = secure_filename(file.filename)
					file.save(f'static/images/{filename}')
			db.change_project(
				request.form['id'],
				request.form['title'],
				request.form['description'],
				filename,
				request.form['url']
			)
			
	projects = db.select_all()
	return render_template("pages/admin_project.html", projects=projects)

@app.route('/admin')
def admin():
	return render_template("pages/admin.html")

@app.errorhandler(404)
def error_not_found(error):
	return f"<h1>Страница не найдена! Илья смотри свой код!</h1> {error}", 404

@app.route("/admin/add_project", methods=['GET', 'POST'])
def admin_add():
	if request.method == "POST":
		for key in request.form:
			if request.form[key] == "":
				flash(["не все поля заполнены!", ["red"]])
				return render_template("admin/add_project.html")
		else:
			file = request.files['file']
			if file and check_file(file.filename):
				filename = secure_filename(file.filename)
				print(filename, flush=True)
				file.save(f'static/images/{filename}')
				db.create_project(
					request.form['title'],
					request.form['description'],
					filename,
					request.form['link']
				)
				flash(['Проект добавлен!', 'green'])
	return render_template('admin/add_project.html')			

if __name__ == "__main__":
	app.run()
